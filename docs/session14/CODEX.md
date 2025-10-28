Excellent — you’re asking for a Codex-ready teaching prompt that matches your existing instructional structure but targets a new Testing, Error Handling, and Optimization theme for your Notifier App.

Here’s your updated Codex prompt, modeled precisely on your previous one but aligned to cover:
	•	Unit & Integration testing (with mocks, setup, and fixtures)
	•	Graceful error handling
	•	Rate limiting & throttling
	•	Caching & session usage

It maintains your “do not modify the app” rule and uses the activity/session14/ folder for safety and version control.

⸻

📘 Prompt for Codex — Create Testing & Optimization Activity Files

(Do NOT Modify App Code)

⸻

🧩 Context

You are assisting a lecturer teaching Session 14: Testing, Error Handling & Optimization in Django (Notifier App) using session14_codex.md as reference.
This session focuses on building testable, maintainable, and performant Django apps through structured testing and optimization practices.

The live teaching project is the Notifier App, which students will extend later in their final project.

The lecturer will explain, demonstrate, and merge any code changes after review.
You must not modify or overwrite any existing app code — all new materials must be placed in a dedicated directory for review.

⸻

⚙️ Strict Instruction

🚫 Do not modify, inject, or replace code in the Notifier App.
✅ All code, markdown explanations, and step-by-step guides must be placed inside:

activity/session14/

✅ Use clear filenames so the lecturer can review before merging:

activity/session14/
├── activity_instructions.md
├── test_unit_example.py
├── test_integration_example.py
├── error_handling_example.py
├── caching_session_example.py
└── throttling_example.py


⸻

🧠 Codex Goal

Generate a teaching activity package that:
	1.	Reinforces Django’s testing and optimization practices in context.
	2.	Uses the Notifier App models, views, and APIs as realistic examples.
	3.	Produces clear, modular examples suitable for live coding and student exercises.
	4.	Places all materials inside the new activity/session14/ folder (not the core app).

⸻

📋 Learning Outcomes

By completing this activity, students will:
	•	Understand unit and integration testing with Django’s TestCase and fixtures.
	•	Use mock objects to isolate dependencies (e.g., email services, ML inferences).
	•	Implement graceful error handling with structured logging and custom exceptions.
	•	Apply rate limiting and throttling rules using DRF configurations.
	•	Configure caching and session usage to optimize performance and reduce DB hits.

⸻

🧱 Codex Instructions

Step 1 — Review

• Read session14_codex.md for theoretical references.
• Review the existing Notifier app models, views, and configurations.

Step 2 — Generate Activities (DO NOT APPLY)

Create new example files under:

activity/session14/

Each file should include commented, self-contained examples demonstrating key testing and optimization techniques.

⸻

🧩 Step 3 — Activity Design

Codex should build instructor-led examples that:
	1.	Introduce the testing or optimization concept being demonstrated.
	2.	Walk through step-by-step instructions with commented code.
	3.	Provide example Django test cases, fixtures, and configurations.
	4.	Show expected console outputs or results.
	5.	End with reflection questions and verification steps.

⸻

🧩 Example Activity Themes

Codex should include at least five themed examples, one per file:

File	Concept	Description
test_unit_example.py	Unit Testing	Demonstrates testing utility functions or views with mock data using unittest.mock.
test_integration_example.py	Integration Testing	Tests full request/response cycles using Django’s test client and sample data.
error_handling_example.py	Graceful Error Handling	Shows structured exception handling, logging, and fallback responses.
throttling_example.py	Rate Limiting & Throttling	Demonstrates DRF throttles, user tiers, and test cases verifying 429 responses.
caching_session_example.py	Caching & Session Usage	Illustrates LocMemCache/FileBasedCache usage and session persistence testing.


⸻

🧩 Expected Output

activity/session14/activity_instructions.md
A formatted markdown guide with:
	•	Overview of testing and optimization goals
	•	Step-by-step coding instructions
	•	Example commands (pytest, python manage.py test, etc.)
	•	Code explanations
	•	Reflection questions (3–4 prompts)
	•	A checklist for students to verify success

⸻

🧩 Example: test_unit_example.py

# activity/session14/test_unit_example.py
from django.test import TestCase
from unittest.mock import patch
from notifier.services import send_notification

class NotificationUnitTests(TestCase):
    @patch("notifier.services.email_backend.send_email")
    def test_send_notification_success(self, mock_send_email):
        mock_send_email.return_value = True
        result = send_notification("user@example.com", "Welcome")
        self.assertTrue(result)
        mock_send_email.assert_called_once()


⸻

🧩 Example: error_handling_example.py

# activity/session14/error_handling_example.py
import logging

logger = logging.getLogger(__name__)

def safe_send_notification(user, message):
    try:
        # Simulated send
        raise ConnectionError("SMTP server unreachable")
    except Exception as e:
        logger.error(f"Failed to send notification: {e}")
        return {"status": "error", "details": str(e)}


⸻

🧩 Example: throttling_example.py

# activity/session14/throttling_example.py
from rest_framework.test import APIClient, APITestCase

class ThrottleTests(APITestCase):
    def test_throttle_limit_reached(self):
        client = APIClient()
        for _ in range(5):
            response = client.get("/api/notify/infer/")
        self.assertEqual(response.status_code, 429)


⸻

🧩 Reflection Questions
	1.	How do mocks help isolate tests from external dependencies?
	2.	What’s the difference between unit and integration testing in Django?
	3.	Why is structured logging important in error handling?
	4.	How does caching differ from throttling in performance management?

⸻

✅ Deliverables for the Lecturer

Codex must output:
	1.	A folder: activity/session14/
	2.	Six reviewed files:
	•	activity_instructions.md
	•	test_unit_example.py
	•	test_integration_example.py
	•	error_handling_example.py
	•	throttling_example.py
	•	caching_session_example.py
	3.	No app file changes.
	4.	A short summary describing the purpose of each file.

⸻

🧭 Tone & Style
	•	Use clear, instructor-ready explanations and comments.
	•	Keep examples small, isolated, and illustrative.
	•	Use realistic Notifier app context and model names.
	•	Output everything as educational scaffolds — never production code.
	•	Maintain consistency with prior session activity structure and markdown formatting.

⸻
