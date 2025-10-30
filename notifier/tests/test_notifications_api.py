import asyncio
import json
from typing import List
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.test import TestCase
from django.urls import reverse

from notifier.models import Document


# Async method replacing fetch_all_metadata
async def fake_metadata_fetch() -> List[str]:
    await asyncio.sleep(0)
    return ["delivered"]


class NotifyViewIntegrationTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="lecturer",
            email="lecturer@example.com",
            password="pass123"
        )
        perm = Permission.objects.get(codename="view_document")
        self.user.user_permissions.add(perm)
        self.client.login(username="lecturer", password="pass123")

    @patch("notifier.views.views.fetch_all_metadata", new=fake_metadata_fetch)
    def test_notify_view_context(self):
        response = self.client.get(reverse("notify"))
        self.assertEqual(response.status_code, 200)
        context = response.context

        self.assertIn("logs", context)
        self.assertIn("user", context)
        self.assertGreater(len(context["logs"]), 0)
        self.assertEqual(context["user"].name, "Ben")
