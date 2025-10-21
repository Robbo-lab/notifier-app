# models/notifications.py
from django.conf import settings
from django.db import models
from notifier.models import Document


class Notification(models.Model):
    """Stores notifications queued or sent to a user."""
    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notifications",
    )
    document = models.ForeignKey(
        Document,
        on_delete=models.PROTECT,
        related_name="notifications",
        null=True,
        blank=True,
    )
    subject = models.CharField(max_length=200)
    message = models.TextField()
    status = models.CharField(
        max_length=20,
        choices=[("draft", "Draft"), ("queued", "Queued"), ("sent", "Sent"), ("failed", "Failed")],
        default="queued",
    )
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    sent_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["recipient", "subject", "created_at"],
                name="unique_notification_per_subject_per_user",
            )
        ]
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.subject} → {self.recipient}"