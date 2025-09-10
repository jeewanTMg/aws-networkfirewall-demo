import os
import json
import boto3
from botocore.exceptions import ClientError

# -----------------------------
# Function to fetch secrets
# -----------------------------
def get_secret(secret_name: str, region_name: str = None) -> dict:
    """
    Fetch a secret from AWS Secrets Manager with error handling and caching.
    """

    # Default region from environment or fallback
    region_name = region_name or os.getenv("AWS_REGION", "us-east-1")

    # Create a boto3 session and client
    session = boto3.session.Session()
    client = session.client("secretsmanager", region_name=region_name)

    try:
        response = client.get_secret_value(SecretId=secret_name)
        secret_str = response.get("SecretString")

        if not secret_str:
            raise ValueError(f"Secret {secret_name} has no SecretString")

        # Parse JSON string to Python dict
        secret_dict = json.loads(secret_str)

        # Cache the secret for future use
        return secret_dict

    except client.exceptions.ResourceNotFoundException:
        print(f"Secret {secret_name} not found in region {region_name}")
    except ClientError as e:
        print(f"AWS ClientError: {e}")
    except json.JSONDecodeError:
        print(f"Secret {secret_name} is not a valid JSON string")
    except Exception as e:
        print(f"Unexpected error fetching secret {secret_name}: {e}")

    return {}  # Return empty dict if any error occurs

# -----------------------------
# Example usage: environment-specific
# -----------------------------
def get_environment() -> str:
    """
    Determine the environment (dev, staging, prod) from env variable.
    """
    return os.getenv("ENV", "dev").lower()


# -----------------------------
# Fetch application credentials
# -----------------------------
def get_app_credentials() -> dict:
    """
    Fetch app-specific secrets for the current environment.
    Example: username/password for an API or service.
    """
    env = get_environment()
    secret_name = f"app-{env}-credentials"
    return get_secret(secret_name)


# -----------------------------
# Fetch database credentials
# -----------------------------
def get_db_credentials() -> dict:
    """
    Fetch database credentials for the current environment.
    Expected keys in secret: username, password, host, port, dbname
    """
    env = get_environment()
    secret_name = f"db-{env}-credentials"
    return get_secret(secret_name)


# -----------------------------
# Example main function
# -----------------------------
if __name__ == "__main__":
    # App credentials
    app_creds = get_app_credentials()
    print("App username:", app_creds.get("username"))
    print("App password:", app_creds.get("password"))

    # Database credentials
    db_creds = get_db_credentials()
    print("DB username:", db_creds.get("username"))
    print("DB password:", db_creds.get("password"))
    print("DB host:", db_creds.get("host"))
    print("DB port:", db_creds.get("port"))
    print("DB name:", db_creds.get("dbname"))
