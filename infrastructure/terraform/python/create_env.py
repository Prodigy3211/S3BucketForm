from botocore.exceptions import ClientError
import boto3


def get_secret_and_write_to_file(secret_name):
    """Get the secret from AWS Secrets Manager and write it to a file."""
    region_name = "us-east-1"
    # Path to the file where you want to save the environment variables
    env_file_path = "app/.env"

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        # For a list of exceptions thrown, see
        # https://docs.aws.amazon.com/secretsmanager
        # /latest/apireference/API_GetSecretValue.html
        raise e

    # Check if the secret was returned as a string
    if 'SecretString' in get_secret_value_response:
        secret = get_secret_value_response['SecretString']

        # Write the secret to a file
        with open(env_file_path, 'w', encoding="UTF-8") as env_file:
            env_file.write(secret)
            print(
                f"Environment variables have been written to {env_file_path}.")
    else:
        # Handle the case where the secret is
        # not a string (e.g., a binary secret)
        print("Secret is not a string.")


# Call the function.
get_secret_and_write_to_file("prod/envs")
