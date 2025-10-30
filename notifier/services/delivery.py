import logging
from dataclasses import dataclass
from django.template.loader import render_to_string

logger = logging.getLogger("activity.session14.errors")

class NotificationDeliveryError(Exception):
    """Raised when a notification cannot be completed."""


@dataclass
class NotificationRequest:
    recipient_email: str
    subject: str
    message: str


# Helper: wraps the delivery attempt and formats a UI response.
def safe_send_notification(request: NotificationRequest, send_callable):
    if not request.recipient_email:
        raise ValueError("Recipient email is required.")

    try:
        message_id = send_callable(request)
    except NotificationDeliveryError as exc:
        logger.error(
            "notification_delivery_failed",
            extra={
                "recipient": request.recipient_email,
                "subject": request.subject,
                "details": str(exc),
            },
        )
        return {
            "status": "error",
            "template": render_to_string(
                "notifier/partials/notification_error.html",
                {
                    "recipient_email": request.recipient_email,
                    "subject": request.subject,
                    "details": str(exc),
                },
            ),
        }

    return {
        "status": "success",
        "message_id": message_id,
    }

