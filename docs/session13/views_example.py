"""
Example class-based view demonstrating how to surface Notification data.
Use this as a reference when integrating the model into the Notifier App.
"""

from django.views.generic import ListView

from .models_example import Notification


class NotificationListView(ListView):
    """
    Displays recent notifications with related recipients and documents preloaded.
    """

    model = Notification
    template_name = "activity/session13/notification_list.html"
    queryset = Notification.objects.select_related("document", "recipient").order_by("-created_at")

    def get_context_data(self, **kwargs):
        """
        Extend the context with simple aggregates for teaching discussion.
        """

        context = super().get_context_data(**kwargs)
        notifications = context["object_list"]
        context["total_sent"] = notifications.filter(status="sent").count()
        context["total_failed"] = notifications.filter(status="failed").count()
        return context
