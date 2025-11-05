from typing import List

from django.contrib.sessions.middleware import SessionMiddleware
from django.core.cache import cache
from django.http import JsonResponse
from django.test import RequestFactory, TestCase
from django.test.utils import override_settings

from notifier.models import Document
from notifier.services.caching import get_cached_document_payload


CACHE_KEY = "activity.session14.documents:list"

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