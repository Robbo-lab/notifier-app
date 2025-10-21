<!-- activity_basic_view.md -->

Activity 1: Basic View and Template Rendering
Learning Objective
Render a template with context data using Django’s render() shortcut.

Step 1: File and Context
Add a dashboard view to the existing notifications app so students land on a welcome page fed by dynamic context.

Step 2: Add the Code

# notifications/views.py

```python
from django.shortcuts import render # Import render helper

def dashboard(request): # Build the context dictionary that template will consume
    context = {
        "page_title": "Notifier Dashboard", # Title shown in the browser tab
        "welcome_message": "Welcome to the notifier control panel!", # Hero text
        "active_alerts": ["Server Load High", "Email Queue Delayed"], # Sample list data
    } # Render the HTML template with the context for this request
    return render(request, "notifications/dashboard.html", context)
```

Expected behaviour: Django will look for notifications/dashboard.html and pass the context variables to it when /dashboard/ is requested.

# notifications/urls.py

```python
from django.urls import path # URL dispatcher helper
from . import views # Import the views module from the same app

urlpatterns = [
  path("dashboard/", views.dashboard, name="dashboard"), # Map URL to the new view
]
```

Expected behaviour: Visiting /dashboard/ now routes to the dashboard view without touching existing patterns.

```html
<!-- templates/notifications/dashboard.html -->

{% extends "base.html" %}
<!-- Reuse global layout if available -->

{% block content %}

<section>
    <h1>{{ page_title }}</h1>
    <!-- Display the title from context -->
    <p>{{ welcome_message }}</p>
    <!-- Show the welcome text -->
    <ul>
        {% for alert in active_alerts %}
        <li>{{ alert }}</li>
        <!-- Loop through alerts -->
        {% empty %}
        <li>No active alerts right now.</li>
        <!-- Fallback when list is empty -->
        {% endfor %}
    </ul>
</section>
{% endblock %}
```

Expected behaviour: The template displays the title, message, and a bullet list populated from the context.

Step 3: Run and Test
Run python manage.py runserver and open http://127.0.0.1:8000/dashboard/.

Step 4: Expected Output
Browser shows the dashboard heading, welcome text, and the two sample alerts rendered as list items.
