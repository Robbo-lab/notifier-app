from django.test import TestCase, RequestFactory, override_settings
from django.contrib.sessions.middleware import SessionMiddleware

from notifier.models import Document
from notifier.services.session_storage import remember_last_document
import json


@override_settings(
    CACHES={
        "default": {
            "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
            "LOCATION": "session14-cache",
        }
    }
)


class SessionPersistenceTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.middleware = SessionMiddleware(lambda request: None)
        self.document = Document.objects.create(
            title="Team Charter",
            description="Rules of AI"
        )

    def _prepare_request(self):
        request = self.factory.post("/session-store/")
        self.middleware.process_request(request)
        request.session.save()
        return request

    def test_remember_last_document_stored_in_session(self):
        request = self._prepare_request()

        response = remember_last_document(request, self.document.title)

        self.assertEqual(response.status_code, 200)
        self.assertIn("last_document_title", request.session)
        self.assertEqual(request.session["last_document_title"], self.document.title)

        payload = json.loads(response.content)
        self.assertEqual(payload["stored"], self.document.title)
