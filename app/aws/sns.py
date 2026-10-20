"""Amazon Simple Notification Service (SNS) adapter for Movie Magic.
Handles booking email notifications and alerts.
"""
import logging
import os
from typing import Dict, Any, Optional
from .client_factory import get_boto3_client

logger = logging.getLogger(__name__)


class SNSService:
    """SNS Service adapter for dispatching booking confirmation notifications."""

    def __init__(self, topic_arn: Optional[str] = None):
        self.topic_arn = topic_arn or os.environ.get("SNS_BOOKING_TOPIC_ARN", "")
        self._client = get_boto3_client("sns")
        self.is_connected = self._client is not None and bool(self.topic_arn)

    def publish_booking_confirmation(self, booking_details: Dict[str, Any]) -> bool:
        """Publish booking confirmation message to SNS topic."""
        booking_id = booking_details.get("booking_id") or booking_details.get("id") or "UNKNOWN"
        message = (
            f"🎬 Movie Magic Booking Confirmation\n"
            f"Booking ID: {booking_id}\n"
            f"Movie: {booking_details.get('movie_title')}\n"
            f"Theater: {booking_details.get('theater_name')}\n"
            f"Showtime: {booking_details.get('showtime')}\n"
            f"Seats: {', '.join(booking_details.get('seats', []))}\n"
            f"Total Amount: ₹{booking_details.get('total_price', 0):.2f}\n"
            f"Status: Confirmed (Demo)\n"
            f"Enjoy your movie!"
        )

        if not self.is_connected:
            logger.info(f"[Mock Mode] SNS notification simulated for booking: {booking_id}")
            return True

        try:
            self._client.publish(
                TopicArn=self.topic_arn,
                Subject=f"Movie Magic Booking Confirmed #{booking_id}",
                Message=message
            )
            return True
        except Exception as e:
            logger.error(f"Failed to publish to SNS: {e}")
            return False
