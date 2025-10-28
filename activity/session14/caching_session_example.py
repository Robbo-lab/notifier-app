# activity/session14/caching_session_example.py
# Linked code: notifier/views/views.py::documents_collection and session usage in notifier/views/views.py::notify_view

from typing import List

from django.contrib.sessions.middleware import SessionMiddleware
from django.core.cache import cache
from django.http import JsonResponse
from django.test import RequestFactory, TestCase
from django.test.utils import override_settings

from notifier.models import Document

CACHE_KEY = "activity.session14.documents:list"


# Cache helper inspired by notifier/views/views.py::documents_collection
def get_cached_document_payload() -> List[dict]:
    def _query():
        documents = Document.objects.order_by("-uploaded_at")
        return [
            {
                "id": doc.id,
                "title": doc.title,
                "description": doc.description,
            }
            for doc in documents
        ]

    return cache.get_or_set(CACHE_KEY, _query, timeout=60)


# Session helper mirroring the user context stored in notifier/views/views.py::notify_view
def remember_last_document(request, document_id: int) -> JsonResponse:
    request.session["last_document_id"] = document_id
    request.session.modified = True
    return JsonResponse({"stored": document_id})


@override_settings(
    CACHES={
        "default": {
            "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
            "LOCATION": "session14-cache",
        }
    }
)
# Tests mirroring notifier/views/views.py::documents_collection caching needs
class DocumentCachingTests(TestCase):
    def setUp(self):
        cache.clear()
        Document.objects.create(title="Run Sheet", description="Agenda")
        Document.objects.create(title="Release Notes", description="Sprint summary")

    def test_document_list_hits_database_once(self):
        with self.assertNumQueries(1):
            first_payload = get_cached_document_payload()

        with self.assertNumQueries(0):
            second_payload = get_cached_document_payload()

        self.assertEqual(first_payload, second_payload)
        self.assertEqual(len(first_payload), 2)


# Tests mirroring session usage from notifier/views/views.py::notify_view
class SessionPersistenceTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.middleware = SessionMiddleware(lambda request: None)
        self.document = Document.objects.create(title="Team Charter", description="Rules of engagement")

    def _prepare_request(self):
        request = self.factory.post("/activities/session14/session-store/")
        self.middleware.process_request(request)
        request.session.save()
        return request

    def test_remember_last_document_stores_in_session(self):
        request = self._prepare_request()

        response = remember_last_document(request, self.document.pk)

        self.assertEqual(response.status_code, 200)
        self.assertIn("last_document_id", request.session)
        self.assertEqual(request.session["last_document_id"], self.document.pk)
        self.assertEqual(response.json()["stored"], self.document.pk)


# Integration sketch (pseudo-code for the main app)
# 1. Introduce `get_cached_document_payload` inside `notifier/views/documents.py`
#    (or a new helper module) and call it from `documents_collection`.
# 2. Invalidate the cache wherever documents are created or modified.
# 3. Use `remember_last_document` logic in the `notify_view` response cycle
#    to persist the chosen document ID in `request.session`.
# 4. Add tests to `notifier/tests/test_caching.py` covering cache hits and session writes.
# 5. Confirm the chosen cache backend in `settings.py` supports the required features
#    (LocMemCache for dev, Redis or Memcached for production).
