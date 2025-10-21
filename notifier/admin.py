from django.contrib import admin
from .models import Notification

# decorator registers the NotificationAdmin class with the admin site.
# automatically configures the admin list page and filters using the tuples.
# renders the correct admin templates (list, change, add, delete) automatically.
@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ("subject", "recipient", "status", "created_at", "sent_at")
    list_filter = ("status", "created_at", "sent_at")
    search_fields = ("subject", "recipient__username", "metadata")
