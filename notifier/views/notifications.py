from django.views.generic import ListView
from notifier.models import Notification
from notifier.services.delivery import NotificationRequest, safe_send_notification, NotificationDeliveryError


class NotificationListView(ListView):
    model = Notification
    queryset = Notification.objects.select_related("document", "recipient")
    template_name = "notifier/notification_list.html"

    # helper method
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        notifications = context["object_list"]
        context["total_queued"] = notifications.filter(status="queued").count()
        context["total_sent"] = notifications.filter(status="sent").count()
        context["total_failed"] = notifications.filter(status="failed").count()

        # Sample usage of safe_send_notification for the first notification
        if notifications:
            sample = notifications.first()
            request = NotificationRequest(
                recipient_email=sample.recipient.email,
                subject=sample.subject,
                message=sample.message
            )

            # Simulated sender function (stub)
            def fake_sender(req):
                raise NotificationDeliveryError("Simulated delivery failure.")

            payload = safe_send_notification(request, fake_sender)
            context["test_notification_result"] = payload

        return context