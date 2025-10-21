<!-- activity_template_inheritance.md -->

Activity 2: Template Inheritance with base.html
Learning Objective
Use Django template inheritance to keep page structure DRY.

Step 1: File and Context
Upgrade the dashboard to extend from a new base.html layout so child templates share the same frame.

Step 2: Add the Code

# watch out for the static import

<!-- templates/base.html -->
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8"> <!-- Ensure proper encoding -->
  <title>{% block title %}Notifier{% endblock %}</title> <!-- Allow child templates to override -->
  <link rel="stylesheet" href="{% static 'css/main.css' %}"> <!-- Shared stylesheet -->
</head>
<body>
  <header>
    <h1>Notifier Control Center</h1> <!-- Always visible banner -->
    <nav>
      <a href="{% url 'dashboard' %}">Dashboard</a> <!-- Navigation example -->
      <a href="{% url 'alerts:upload' %}">Upload CSV</a> <!-- Placeholder for later activity -->
    </nav>
  </header>

  <main>
    {% block content %}{% endblock %} <!-- Child templates inject content -->
  </main>

  <footer>
    <small>&copy; {{ now|date:"Y" }} Notifier</small> <!-- Dynamic year display -->
  </footer>
</body>
</html>

<!-- templates/notifications/dashboard.html -->

{% extends "base.html" %} <!-- Opt into the shared layout -->

{% block title %}Dashboard | Notifier{% endblock %} <!-- Customize tab title -->

{% block content %}

  <section>
    <h2>{{ page_title }}</h2> <!-- Page-specific heading -->
    <p>{{ welcome_message }}</p> <!-- Page-specific paragraph -->
    <ul>
      {% for alert in active_alerts %}
        <li>{{ alert }}</li>
      {% endfor %}
    </ul>
  </section>
{% endblock %}

Step 3: Run and Test
Execute python manage.py runserver and refresh http://127.0.0.1:8000/dashboard/.

Step 4: Expected Output
Page now shows the global header, navigation, and footer surrounding the dashboard content.
