# activity/session14/throttling_example.py
# Linked code: notifier/services and planned background jobs that trigger notifications

from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.test import TestCase
from django.test.utils import override_settings

from rest_framework.test import APIRequestFactory, force_authenticate
from rest_framework.throttling import UserRateThrottle


# Custom throttle used when a lecturer triggers bulk notifications
class DocumentTriggerThrottle(UserRateThrottle):
    scope = "document_trigger"


# Stub callable representing the expensive work triggered by the lecturer
def trigger_notification_workflow(request, throttle=None):
    throttle = throttle or DocumentTriggerThrottle()
    if not throttle.allow_request(request, view=None):
        return {"status": "throttled"}
    return {"status": "accepted"}


@override_settings(
    REST_FRAMEWORK={
        "DEFAULT_THROTTLE_RATES": {
            "document_trigger": "3/min",
        }
    }
)
# Tests for the manual notification trigger workflow used by lecturers
class ThrottlingExampleTests(TestCase):
    def setUp(self):
        cache.clear()
        self.factory = APIRequestFactory()
        self.user = get_user_model().objects.create_user(
            username="lecturer",
            email="lecturer@example.com",
            password="pa55-word",
        )
        self.throttle = DocumentTriggerThrottle()

    # Tests focused on throttling the lecture-triggered notification workflow
    def test_trigger_notification_workflow_throttles_after_three_calls(self):
        responses = []
        for _ in range(3):
            request = self.factory.post("/tasks/trigger/")
            force_authenticate(request, user=self.user)
            responses.append(trigger_notification_workflow(request, throttle=self.throttle))

        throttled_request = self.factory.post("/tasks/trigger/")
        force_authenticate(throttled_request, user=self.user)
        throttled_response = trigger_notification_workflow(throttled_request, throttle=self.throttle)

        self.assertTrue(all(response["status"] == "accepted" for response in responses))
        self.assertEqual(throttled_response["status"], "throttled")


# Integration sketch (pseudo-code for the main app)
# 1. Place `DocumentTriggerThrottle` in `notifier/throttling.py` (new module).
# 2. Import the throttle into the view or service that triggers notifications.
# 3. Configure the matching scope ("document_trigger") inside `REST_FRAMEWORK`
#    in `notifier_core/settings.py`.
# 4. If the workflow runs outside DRF, construct a `rest_framework.request.Request`
#    or adapt this pattern to DRF views so the throttle can read the user.
# 5. Add a regression test in `notifier/tests/test_throttling.py` using the APIClient
#    or request factory that matches the production entry point.
