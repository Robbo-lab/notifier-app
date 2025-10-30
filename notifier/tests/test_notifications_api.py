import asyncio
import json
from typing import List
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.test import TestCase
from django.urls import reverse

from notifier.models import Document


# Async stub mirroring notifier/utils/metadata.py::fetch_all_metadata
async def fake_metadata_fetch() -> List[str]:
    await asyncio.sleep(0)
    return ["stubbed"]


# Tests for notifier/views/views.py::notify_view
class NotifyViewIntegrationTests(TestCase):
    def setUp(self):
        user_model = get_user_model()
        self.password = "pa55-word"
        self.user = user_model.objects.create_user(
            username="lecturer",
            email="lecturer@example.com",
            password=self.password,
        )
        permission = Permission.objects.get(codename="view_document")
        self.user.user_permissions.add(permission)
        assert self.client.login(username=self.user.username, password=self.password)

    def test_notify_view_renders_context_safely(self):
        with self.assertLogs(level="INFO") as captured_logs:
            with patch("notifier.views.views.fetch_all_metadata", new=fake_metadata_fetch):
                response = self.client.get(reverse("notify"))

        self.assertEqual(response.status_code, 200)
        self.assertIn("logs", response.context)
        self.assertIn("user", response.context)
        self.assertGreater(len(response.context["logs"]), 0)
        self.assertEqual(response.context["user"].name, "Ben")
        self.assertTrue(any("[ACTION]" in line for line in captured_logs.output))


# Tests for notifier/urls.py::documents_collection and notifier/views/views.py::document_detail
class DocumentApiIntegrationTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.payload = {
            "title": "Release Notes",
            "description": "Sprint 14 summary for stakeholders.",
        }

    def test_document_crud_flow(self):
        create_response = self.client.post(
            reverse("documents_collection"),
            data=json.dumps(self.payload),
            content_type="application/json",
        )
        self.assertEqual(create_response.status_code, 201)
        document_id = create_response.json()["id"]

        list_response = self.client.get(reverse("documents_collection"))
        self.assertEqual(list_response.status_code, 200)
        documents = list_response.json()["documents"]
        self.assertEqual(len(documents), 1)

        detail_response = self.client.get(reverse("document_detail", args=[document_id]))
        self.assertEqual(detail_response.status_code, 200)
        self.assertEqual(detail_response.json()["title"], self.payload["title"])

        delete_response = self.client.delete(reverse("document_detail", args=[document_id]))
        self.assertEqual(delete_response.status_code, 204)
        self.assertFalse(Document.objects.filter(pk=document_id).exists())