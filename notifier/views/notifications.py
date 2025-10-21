from django.views.generic import ListView
from notifier.models import Notification


class NotificationListView(ListView):
    model = Notification
    queryset = Notification.objects.select_related("document", "recipient")
    template_name = "notifier/notification_list.html"