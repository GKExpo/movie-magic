"""DynamoDB service interface and adapter for Movie Magic.
In Phase 1, provides the exact method contract for Phase 2 DynamoDB integration.
"""
import logging
import os
from typing import Any, Dict, List, Optional
from .client_factory import get_boto3_client

logger = logging.getLogger(__name__)


class DynamoDBService:
    """DynamoDB service adapter.
    Encapsulates AWS DynamoDB calls and provides structured fallbacks for Phase 1.
    """

    def __init__(self, table_prefix: Optional[str] = None):
        self.table_prefix = table_prefix or os.environ.get("DYNAMODB_TABLE_PREFIX", "moviemagic_")
        self._client = get_boto3_client("dynamodb")
        self.is_connected = self._client is not None

    def get_table_name(self, base_name: str) -> str:
        return f"{self.table_prefix}{base_name}"

    def put_item(self, table_name: str, item: Dict[str, Any]) -> bool:
        """Put an item into DynamoDB table."""
        full_table_name = self.get_table_name(table_name)
        if not self.is_connected:
            logger.info(f"[Phase 1 Demo] DynamoDB.put_item stub called for {full_table_name} with {len(item)} attributes.")
            return True

        try:
            self._client.put_item(TableName=full_table_name, Item=item)
            return True
        except Exception as e:
            logger.error(f"Error putting item into {full_table_name}: {e}")
            return False

    def get_item(self, table_name: str, key: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Retrieve an item by primary key."""
        full_table_name = self.get_table_name(table_name)
        if not self.is_connected:
            logger.info(f"[Phase 1 Demo] DynamoDB.get_item stub called for {full_table_name} with key {key}.")
            return None

        try:
            response = self._client.get_item(TableName=full_table_name, Key=key)
            return response.get("Item")
        except Exception as e:
            logger.error(f"Error getting item from {full_table_name}: {e}")
            return None
