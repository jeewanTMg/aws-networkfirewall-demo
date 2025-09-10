import json
import boto3
import boto3.session

print(boto3.__version__)

def get_secret(secret_name):
    region_name = "us-east-1"

    # Creating the Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name="secretsmanager",
        region_name=region_name
    )

    get_secret_value_response = client.get_secret_value(SecretId=secret_name)

    # Use json.loads instead of json.load
    secret = json.loads(get_secret_value_response['SecretString'])
    result = secret["username"]
    print(result)

get_secret("aws-test-env")
