"""Centralized AWS Client Factory.

Provides boto3 client generation with graceful fallback for local development.
Never hardcodes AWS credentials or requires active cloud access in Phase 1.
"""
import logging
import os
import boto3
from botocore.exceptions import BotoCoreError, NoCredentialsError

logger = logging.getLogger(__name__)


def is_aws_configured() -> bool:
    """Check if basic AWS credentials/region are present in environment."""
    region = os.environ.get("AWS_REGION")
    access_key = os.environ.get("AWS_ACCESS_KEY_ID")
    secret_key = os.environ.get("AWS_SECRET_ACCESS_KEY")
    use_mock = os.environ.get("USE_AWS_MOCK", "True").lower() in ("true", "1", "yes")

    if use_mock:
        return False
    return bool(region and access_key and secret_key)


def get_boto3_client(service_name: str):
    """Safely obtain a boto3 client or None if AWS is not configured or mock mode is active.

    Args:
        service_name: 'dynamodb', 'sns', etc.

    Returns:
        boto3 client or None
    """
    use_mock = os.environ.get("USE_AWS_MOCK", "True").lower() in ("true", "1", "yes")
    if use_mock:
        logger.debug(f"[AWS Stub] USE_AWS_MOCK is True. Skipping real {service_name} client creation.")
        return None

    region = os.environ.get("AWS_REGION", "us-east-1")
    access_key = os.environ.get("AWS_ACCESS_KEY_ID")
    secret_key = os.environ.get("AWS_SECRET_ACCESS_KEY")

    try:
        kwargs = {"region_name": region}
        if access_key and secret_key:
            kwargs["aws_access_key_id"] = access_key
            kwargs["aws_secret_access_key"] = secret_key

        client = boto3.client(service_name, **kwargs)
        return client
    except (BotoCoreError, NoCredentialsError) as e:
        logger.warning(f"Could not initialize real AWS {service_name} client: {e}. Falling back to mock mode.")
        return None
