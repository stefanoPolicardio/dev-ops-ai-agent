import boto3
import json
import os

def get_rds_credentials():
    secret_name = os.getenv("RDS_SECRET_NAME")
    region = os.getenv("AWS_REGION", "us-east-1")
    client = boto3.client("secretsmanager", region_name=region)
    secret = client.get_secret_value(SecretId=secret_name)
    return json.loads(secret["SecretString"])
