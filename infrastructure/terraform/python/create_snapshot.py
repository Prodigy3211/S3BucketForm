from datetime import datetime
import boto3
import os


def create_rds_snapshot(db_instance_identifier, snapshot_identifier):
    try:
        # Create RDS client
        rds_client = boto3.client('rds', region_name='us-east-1')

        # Create snapshot
        print(f"Creating snapshot: {snapshot_identifier}")
        response = rds_client.create_db_snapshot(
            DBSnapshotIdentifier=snapshot_identifier,
            DBInstanceIdentifier=db_instance_identifier
        )

        # Wait for the snapshot to be available
        print("Waiting for snapshot to be available...")
        waiter = rds_client.get_waiter('db_snapshot_available')
        waiter.wait(
            DBSnapshotIdentifier=snapshot_identifier,
            WaiterConfig={
                'Delay': 30,  # Check every 30 seconds
                'MaxAttempts': 60  # Wait up to 30 minutes (60 * 30 seconds)
            }
        )

        # Get final snapshot details
        snapshot_details = rds_client.describe_db_snapshots(
            DBSnapshotIdentifier=snapshot_identifier
        )

        print("\nSnapshot created successfully!")
        print(f"Snapshot Identifier: {snapshot_identifier}")
        print(f"Status: {snapshot_details['DBSnapshots'][0]['Status']}")
        print(f"Creation Time: {snapshot_details['DBSnapshots'][0]['SnapshotCreateTime']}")

    except rds_client.exceptions.DBSnapshotAlreadyExistsFault:
        print(f"Error: Snapshot with identifier {snapshot_identifier} already exists")
    except Exception as e:
        print(f"Error creating snapshot: {str(e)}")


if __name__ == "__main__":
    github_env = os.environ.get('GITHUB_ENV')
    commit_id = os.environ.get('commit_id')
    env = os.environ.get('ENV')

    db_instance_identifier = f"greatnight{env}"
    timestamp = datetime.now().strftime('%Y-%m-%d')
    snapshot_identifier = f'{db_instance_identifier}-before-{commit_id}-{timestamp}'

    create_rds_snapshot(db_instance_identifier, snapshot_identifier)
