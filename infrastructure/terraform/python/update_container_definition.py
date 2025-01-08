import json
import sys
import os
import subprocess


def parse_tfvars(file_path):
    variables = {}
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if "=" in line and not line.startswith("#"):  # Ignore comments
                key, value = line.split("=", 1)
                key = key.strip()
                value = value.strip().strip('"')
                variables[key] = value
    return variables


def get_latest_image_sha(repository_name):
    """Get the SHA256 digest of the latest image from AWS ECR."""
    try:
        cmd = [
            "aws", "ecr", "describe-images",
            "--repository-name", repository_name,
            "--image-ids", "imageTag=latest",
            "--query", "imageDetails[0].imageDigest",
            "--output", "text"
        ]
        result = subprocess.run(
            cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )
        sha_value = result.stdout.strip()
        return sha_value
    except subprocess.CalledProcessError as e:
        print(f"Error fetching image SHA for {repository_name}: {e.stderr}")
        return None


def main():
    tfvars_file_path = os.environ.get('TF_VARS_FILE')
    if not tfvars_file_path:
        raise ValueError("The TF_VARS_FILE environment variable is not set.")

    variables = parse_tfvars(tfvars_file_path)
    env = variables.get('ecr_repo')

    if not env:
        print("Missing required 'env' variable in .tfvars file.")
        sys.exit(1)

    print(f"Updating container-definition.json for environment: {env}")

    script_dir = os.path.dirname(os.path.abspath(__file__))
    JSON_FILE_PATH = os.path.join(script_dir, '..', 'container-definition.json')

    # Read the existing JSON content
    with open(JSON_FILE_PATH, 'r', encoding="UTF-8") as file:
        data = json.load(file)

    # Update the 'image' field with the new SHA256 value
    for container in data:
        repo_name = env  # Use the environment name as the repository name
        sha_value = get_latest_image_sha(repo_name)
        if sha_value:
            container["image"] = container["image"].replace("sha_value", sha_value)
        else:
            print(f"Failed to update SHA for {repo_name}")

    # Write the updated JSON content back to the file
    with open(JSON_FILE_PATH, 'w', encoding="UTF-8") as file:
        json.dump(data, file, indent=2)

    print("Updated container-definition.json with new SHA256 value.")


if __name__ == "__main__":
    main()
