# Session 14 Activity: Testing, Error Handling & Optimisation

Use the Notifier App as the reference point while exploring isolated tests, end-to-end flows, and performance-minded helpers. All supporting material is contained in `activity/session14/` for pre-lesson review.

## Learning Outcomes
- Distinguish between unit and integration strategies in Django and apply mocks wisely.
- Deliver user-facing fallbacks when notification workflows fail.
- Calibrate throttling rules to protect expensive notification triggers.
- Optimise document lookups and session storage for responsive dashboards.

## Running the Examples

```bash
python manage.py test activity.session14.test_unit_example
python manage.py test activity.session14.test_integration_example
python manage.py test activity.session14.error_handling_example
python manage.py test activity.session14.throttling_example
python manage.py test activity.session14.caching_session_example
```

## File Highlights
- `test_unit_example.py` — mirrors `serialise_document` and `upload_document` so you can demonstrate mocking and pure helper assertions.
- `test_integration_example.py` — drives `notify_view` with permissions plus the document API CRUD flow to capture full-stack behaviour.
- `error_handling_example.py` — keeps the notification dataclass while generating a reusable UI template when delivery fails.
- `throttling_example.py` — applies a `UserRateThrottle` to a manual workflow trigger without wiring REST routes.
- `caching_session_example.py` — caches the document list payload and verifies session persistence with `SessionMiddleware`.

## Integration Playbook (Pseudo Steps)
- Unit tests → copy the two classes into `notifier/tests/test_notifications_unit.py`, keep the `notifier.views.views` import, and run `python manage.py test notifier.tests.test_notifications_unit`.
- Integration tests → move the sample tests into `notifier/tests/test_views_integration.py`, reuse project fixtures, and ensure the async metadata patch targets the production import path.
- Error handling → port the dataclass and helper into `notifier/services/delivery.py`, render the HTML through a new template partial, and call the helper from `notify_view`.
- Throttling → define `DocumentTriggerThrottle` inside a `notifier/throttling.py` module, reference it from the triggering workflow, and add the scope to `REST_FRAMEWORK` settings.
- Caching & sessions → embed the cache helper inside the documents view module, invalidate keys on create/update/delete, and persist the chosen document ID via session writes in `notify_view`.
