# activity/session14/error_handling_example.py
# Linked code: notifier/views/views.py::notify_view and notifier/templates/notifier/index.html (UI messaging)

import logging
from dataclasses import dataclass

from django.test import TestCase

logger = logging.getLogger("activity.session14.errors")


class NotificationDeliveryError(Exception):
    """Raised when a notification cannot be completed."""


@dataclass
class NotificationRequest:
    recipient_email: str
    subject: str
    body: str


# UI-ready template snippet for notifier/templates/notifier/index.html
ERROR_TEMPLATE = """
<div class="notification-error">
  <h2>Delivery issue</h2>
  <p>We could not reach {recipient_email} about "{subject}".</p>
  <p class="details">{details}</p>
  <p>Please retry later or contact support.</p>
</div>
""".strip()


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
            "template": ERROR_TEMPLATE.format(
                recipient_email=request.recipient_email,
                subject=request.subject,
                details=str(exc),
            ),
        }

    return {
        "status": "success",
        "message_id": message_id,
    }


# Tests for the error handling helper that mirrors notifier/services usage
class ErrorHandlingExamples(TestCase):
    def setUp(self):
        self.request = NotificationRequest(
            recipient_email="student@example.com",
            subject="Session 14 Reminder",
            body="Audit your tests before stand-up.",
        )

    def test_safe_send_notification_handles_success(self):
        def send_callable(request):
            return "message-123"

        payload = safe_send_notification(self.request, send_callable)

        self.assertEqual(payload["status"], "success")
        self.assertEqual(payload["message_id"], "message-123")

    def test_safe_send_notification_returns_template_on_error(self):
        def failing_sender(request):
            raise NotificationDeliveryError("Notification service unavailable.")

        with self.assertLogs(logger.name, level="ERROR") as captured:
            payload = safe_send_notification(self.request, failing_sender)

        self.assertEqual(payload["status"], "error")
        self.assertIn("notification-error", payload["template"])
        self.assertIn(self.request.subject, payload["template"])
        self.assertTrue(any("notification_delivery_failed" in line for line in captured.output))


# Integration sketch (pseudo-code for the main app)
# 1. Add `NotificationDeliveryError`, `NotificationRequest`, and `safe_send_notification`
#    to a new module `notifier/services/delivery.py`.
# 2. Register a Django template partial `notifier/partials/notification_error.html`
#    and move `ERROR_TEMPLATE` markup into that file.
# 3. Update `notify_view` to call `safe_send_notification` before rendering the template
#    and pass the returned payload into the context.
# 4. Add tests to `notifier/tests/test_error_handling.py` mirroring the cases above.
# 5. Wire structured logging by configuring the `activity.session14.errors` logger
#    under `LOGGING` in `notifier_core/settings.py`.
