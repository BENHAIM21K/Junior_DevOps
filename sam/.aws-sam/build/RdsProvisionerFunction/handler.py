import json
import boto3
import os
import subprocess
import tempfile
import uuid
from github import Github

def lambda_handler(event, context):
    print("Received event:", json.dumps(event))

    # Get message from SQS
    message = json.loads(event['Records'][0]['body'])
    print("Raw SQS Message:", message)

    # If the message came from SNS, unwrap it
    if 'Message' in message:
        message = json.loads(message['Message'])

    db_name = message['db_name']
    engine = message['engine']
    env = message['env']

    github_token = os.environ['GITHUB_TOKEN']
    repo_name = os.environ['GITHUB_REPO']

    # Setup Git
    github = Github(github_token)
    repo = github.get_repo(repo_name)
    branch_name = f"provision-{db_name}-{uuid.uuid4().hex[:6]}"
    base_branch = "main"

    # Clone the repo into temp dir
    with tempfile.TemporaryDirectory() as tempdir:
        repo_url = f"https://{github_token}@github.com/{repo_name}.git"
        subprocess.run(["git", "clone", "--branch", base_branch, repo_url, tempdir], check=True)

        # Create a new branch
        subprocess.run(["git", "-C", tempdir, "checkout", "-b", branch_name], check=True)

        # Write the Terraform file
        terraform_path = os.path.join(tempdir, "terraform", "rds_module", "main.tf")
        with open(terraform_path, "w") as tf:
            tf.write(f'''
variable "db_name" {{
  default = "{db_name}"
}}

variable "engine" {{
  default = "{engine}"
}}

variable "env" {{
  default = "{env}"
}}

variable "db_secret_name" {{
  default = "rds/credentials"
}}

module "rds" {{
  source           = "./rds_module"
  db_name          = var.db_name
  engine           = var.engine
  env              = var.env
  db_secret_name   = var.db_secret_name
}}
''')

        # Commit and push
        subprocess.run(["git", "-C", tempdir, "add", "."], check=True)
        subprocess.run(["git", "-C", tempdir, "commit", "-m", f"Add RDS cluster for {db_name}"], check=True)
        subprocess.run(["git", "-C", tempdir, "push", "--set-upstream", "origin", branch_name], check=True)

    # Create the pull request
    pr = repo.create_pull(
        title=f"Provision RDS cluster: {db_name}",
        body=f"Provisioning request for `{db_name}` ({engine}, {env})",
        head=branch_name,
        base=base_branch
    )

    print(f"Pull request created: {pr.html_url}")

    return {
        'statusCode': 200,
        'body': json.dumps(f"PR created: {pr.html_url}")
    }
