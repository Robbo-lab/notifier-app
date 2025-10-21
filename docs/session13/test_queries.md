# Django Shell Exercises — Notification

### 1. Load the Django shell
```bash
python manage.py shell
```

### 2. Create a notification
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
    subject="Policy update",
    message="A new document has been uploaded.",
    status="queued",
    metadata={"provider": "email"},
)

print(Notification.objects.count())  # Expect 1 on fresh database
```

### 3. Observe the uniqueness constraint
```python
duplicate_notification = Notification(
    recipient=user,
    document=document,
    subject="Policy update",
    message="Duplicate subject for the same recipient.",
    status="queued",
)
duplicate_notification.full_clean()  # Raises ValidationError before saving
```

### 4. Mark as sent with helper
```python
notification.mark_as_sent()
print(notification.status, notification.sent_at is not None)  # Expect: sent True
```

### 5. Query with ordering and filtering
```python
Notification.objects.order_by("-created_at").values("subject", "status")[:5]
Notification.objects.filter(status="failed").count()
```

### 6. Clean up (optional in a shared training database)
```python
Notification.objects.filter(recipient=user, document=document).delete()
```
