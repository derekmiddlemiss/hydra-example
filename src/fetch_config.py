import boto3
import os

s3_client = boto3.client('s3')


def fetch_config() -> None:
    config_bucket = os.environ["CONFIG_BUCKET"]
    env_prefix = os.environ["SPM_ENV"]
    config_directory = "./config"

    if not os.path.exists(config_directory):
        os.makedirs(config_directory)

    paginator = s3_client.get_paginator('list_objects_v2')
    pages = paginator.paginate(Bucket=config_bucket, Prefix=env_prefix)

    for page in pages:
        if 'Contents' in page:
            for obj in page['Contents']:
                s3_key = obj['Key']
                local_file_path = os.path.join(config_directory, os.path.basename(s3_key))

                # Download the file
                print(f"Downloading {s3_key} to {local_file_path}")
                s3_client.download_file(Bucket=config_bucket, Key=s3_key, Filename=local_file_path)
