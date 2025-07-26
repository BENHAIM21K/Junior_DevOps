import json
import boto3
import os
import tempfile
import uuid
from github import Github, InputGitAuthor

def lambda_handler(event, context):
    print("Received event:", json.dumps(event))

    # Step 1: Extract and unwrap SQS message (SNS inside SQS)
    message = json.loads(event['Records'][0]['body'])
    if 'Message' in message:
        message = json.loads(message['Message'])

    db_name = message['db_name']
    engine = message['engine']
    env = message['env']

    github_token = os.environ['GITHUB_TOKEN']
    repo_name = os.environ['GITHUB_REPO']
    github = Github(github_token)
    repo = github.get_repo(repo_name)

    base_branch = "main"
    unique_suffix = uuid.uuid4().hex[:6]
    new_branch_name = f"provision-{db_name}-{unique_suffix}"

    # Step 2: Get SHA of the base branch
    base = repo.get_branch(base_branch)
    base_sha = base.commit.sha

    # Step 3: Create a new branch from base
    repo.create_git_ref(ref=f"refs/heads/{new_branch_name}", sha=base_sha)

    # Step 4: Define Terraform content
    terraform_code = f'''
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
'''

    # Step 5: Path to update in the repo
    tf_path = "terraform/rds_module/main.tf"

    # Step 6: Read current file SHA (if exists)
    try:
        existing_file = repo.get_contents(tf_path, ref=base_branch)
        repo.update_file(
            path=tf_path,
            message=f"Update RDS provisioning for {db_name}",
            content=terraform_code,
            sha=existing_file.sha,
            branch=new_branch_name,
        )
    except:
        # If file doesn't exist yet, create it
        repo.create_file(
            path=tf_path,
            message=f"Create RDS provisioning for {db_name}",
            content=terraform_code,
            branch=new_branch_name,
        )

    # Step 7: Open PR
    pr = repo.create_pull(
        title=f"Provision RDS cluster: {db_name}",
        body=f"Auto-generated PR to provision RDS cluster with engine `{engine}` in `{env}` environment.",
        head=new_branch_name,
        base=base_branch,
    )

    print(f"Pull request created: {pr.html_url}")

    return {
        "statusCode": 200,
        "body": json.dumps({"pr_url": pr.html_url})
    }
