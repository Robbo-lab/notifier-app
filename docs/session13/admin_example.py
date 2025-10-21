"""
Example admin registration for the Notification teaching model.
Copy into notifier/admin.py after introducing the model to the real project.
"""

from django.contrib import admin

from .models_example import Notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    """
    Lightweight admin configuration highlighting list, filter, and search features.
    """

    list_display = ("subject", "recipient", "status", "created_at", "sent_at")
    list_filter = ("status", "created_at", "sent_at")
    search_fields = (
        "subject",
        "recipient__username",
        "metadata",
    )
    ordering = ("-created_at",)
