# Session 13 Activity — Building a `Notification` Feature with Django ORM

1. sketch the `Notification` model.
2. Highlight relationship fields: `recipient` (Django’s default auth user) and optional `document` (the current Notifier model)
3. tracking with `choices`, metadata captured via `JSONField`, and automatic timestamps for creation and sending.
4. `UniqueConstraint` to prevent duplicate notifications per recipient/subject combination and `ordering` to display the latest events first.
5. integrate class beneath `Document` inside `notifier/models.py`. If you decide to split models into a package later, remember to re-export the class via `notifier/models/__init__.py`.
6. Call the optional `mark_as_sent` helper in the Django shell or admin actions.

```python
# notifier/models/__init__.py
from .document import Document  # existing model
from .notifications import Notification  # re-export so Django can auto-discover the new model
```

```python
# models_example.py
from django.conf import settings
from django.db import models
from django.utils import timezone
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
                fields=["recipient", "subject"],
                name="unique_subject_per_user",
            )
        ]
        ordering = ["-created_at"]

    def mark_as_sent(self, timestamp=None):
        self.status = "sent"
        self.sent_at = timestamp or timezone.now()
        self.save(update_fields=["status", "sent_at"])

    def __str__(self) -> str:
        return f"{self.subject} → {self.recipient}"
```

**Move the Document model & export it**

### 2. Migrate

```bash
python manage.py makemigrations notifier
python manage.py migrate
```

Discuss how Django builds SQL operations, show the generated migration, and highlight rollback safety with `python manage.py migrate notifier 0001`.

### 3. Admin Registration
1. Open a new helper file to outline the admin setup.
2. Keep the admin registration minimal for clarity, show improvements (filters, list displays) once merged into the real project.

```python
# admin.py
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
```

3. Show how the Admin interface sshow the model & CRUD

### 4. Create and Import a View Class
1. class-based view that surfaces notifications. 
2. fix the imports required when the model lives in the same app.
3. add the helper method

```python
# notifier/views/notifications.py
from django.views.generic import ListView
from notifier.models import Notification


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
        return context
```

2. Make the view importable by exposing it in `notifier/views/__init__.py`:

```python
from .notifications import NotificationListView
```

If you keep everything inside `notifier/views.py`, expose the class directly there and import it from `.views` in `urls.py`.

3. Wire it into `notifier/urls.py` for demonstration:

```python
from django.urls import path
from notifier.views import NotificationListView

urlpatterns = [
    path("notifications/", NotificationListView.as_view(), name="notification_list"),
]
```
4. notifier/views/__init__.py
```python
# re-export
from .notifications import NotificationListView
from .views import *
```

### 5. Quick ORM Verification
Use the Django shell to create records and test the constraints

```bash
python manage.py shell
```

```python
from django.contrib.auth import get_user_model
from notifier.models import Document
from activity.session13.models_example import Notification

User = get_user_model()
user = User.objects.first()
document = Document.objects.first()
notification = Notification.objects.create(
    recipient=user,
    document=document,
    subject="Assessment update",
    message="A new document has been uploaded.",
    status="queued",
    metadata={"delivery": "email"},
)

print(Notification.objects.count())  # Expect 1 on a fresh database
notification.mark_as_sent()
print(notification.status, notification.sent_at is not None)  # Expect: sent True

duplicate_notification = Notification(
    recipient=user,
    document=document,
    subject="Assessment update",
    message="Duplicate subject for the same recipient.",
    status="queued",
)
duplicate_notification.full_clean()  # Raises ValidationError before saving

Notification.objects.order_by("-created_at").values("subject", "status")[:5]
```
Use the Django shell to test the helper method

```python

from django.test import RequestFactory
from notifier.views import NotificationListView

factory = RequestFactory()
request = factory.get("/notifications/")

view = NotificationListView()
view.setup(request)
view.object_list = view.get_queryset()
context = view.get_context_data()
print(context["total_queued"],context["total_sent"], context["total_failed"])
```

##  Notes
- `ForeignKey` ensures each notification related to default auth model and may reference a related document.
- `JSONField` stores transport metadata (channel, error codes) without altering schema for new keys.
- `UniqueConstraint` limits duplicate notifications - recipient/subject combination.
- `mark_as_sent` demonstrates how helper methods encapsulate common transitions for shell demos.
- `Meta.ordering` keeps recent notifications on top in Admin and QuerySets, while the companion view precomputes totals for quick status insights.
- In NotificationAdmin.get_queryset, add select_related("recipient", "document") so each row already has those FK objects when the template renders subject, recipient, etc.

