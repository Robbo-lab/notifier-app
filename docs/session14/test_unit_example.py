# activity/session14/test_unit_example.py
# Linked code: notifier/views/views.py::serialise_document and notifier/views/views.py::upload_document

from datetime import datetime, timezone as dt_timezone
from types import SimpleNamespace
from unittest.mock import patch

from django.test import TestCase
from notifier.views import views as notifier_views


# Helper: mirrors Document attributes without touching the ORM.
def build_stub_document() -> SimpleNamespace:
    uploaded_at = datetime(2024, 1, 15, 9, 30, 0, tzinfo=dt_timezone.utc)
    return SimpleNamespace(
        id=42,
        title="Run Sheet",
        description="Agenda for the compliance team.",
        uploaded_at=uploaded_at,
    )


# Tests for notifier/views/views.py::serialise_document
class SerialiseDocumentTests(TestCase):
    def test_serialise_document_formats_payload(self):
        document = build_stub_document()

        payload = notifier_views.serialise_document(document)

        self.assertEqual(payload["id"], document.id)
        self.assertEqual(payload["title"], document.title)
        self.assertEqual(payload["description"], document.description)
        self.assertEqual(payload["uploaded_at"], "2024-01-15T09:30:00Z")


# Tests for notifier/views/views.py::upload_document
class UploadDocumentTests(TestCase):
    @patch("notifier.views.views.notifier.notify")
    def test_upload_document_notifies_once(self, mock_notify):
        user_stub = SimpleNamespace(name="Alex Admin", role=lambda: "admin")

        notifier_views.upload_document(user_stub, "sprint_notes.pdf")

        mock_notify.assert_called_once_with("sprint_notes.pdf")


# Integration sketch (pseudo-code for the main app)
# 1. Create `notifier/tests/test_notifications_unit.py`.
# 2. Paste `SerialiseDocumentTests` and `UploadDocumentTests` into that file.
# 3. Replace `build_stub_document` with a factory or fixture if desired.
# 4. Ensure the module import stays `from notifier.views import views as notifier_views`.
# 5. Run `python manage.py test notifier.tests.test_notifications_unit`.
