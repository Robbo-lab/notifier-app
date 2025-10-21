<!-- activity_chartjs_visualization.md -->
Activity 6: Rendering a Chart.js Visualization
Learning Objective
Display aggregated recipient stats using Chart.js fed from Django context data.

Step 1: File and Context
Visualize the count of recipients by domain on the dashboard using Chart.js.

Step 2: Add the Code
# notifications/views.py
```python
def dashboard(request):
    context = {
        "page_title": "Notifier Dashboard",
        "welcome_message": "Welcome to the notifier control panel!",
        "active_alerts": ["Server Load High", "Email Queue Delayed"],
        # Aggregate data prepared server-side
        "domain_labels": ["example.com", "school.edu", "vendor.net"],
        "domain_counts": [25, 10, 8],
    }
    return render(request, "notifications/dashboard.html", context)
```
Expected behaviour: Context now includes labels and counts for Chart.js to consume.


<!-- templates/notifications/dashboard.html -->
{% extends "base.html" %}

{% block title %}Dashboard | Notifier{% endblock %}

{% block content %}
  <section>
    <h2>{{ page_title }}</h2>
    <p>{{ welcome_message }}</p>
    <canvas id="domainChart" width="400" height="200"></canvas> <!-- Chart mount point -->
  </section>
  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script> <!-- Load Chart.js CDN -->
  <script>
    // Grab canvas element
    const ctx = document.getElementById("domainChart");
    // Instantiate chart with data from context (auto-escaped)
    new Chart(ctx, {
      type: "bar", // Vertical bar chart
      data: {
        labels: {{ domain_labels|safe }}, // Safe to inject JSON-style array
        datasets: [{
          label: "Recipients per Domain", // Legend label
          data: {{ domain_counts|safe }}, // Count values
          backgroundColor: ["#2563eb", "#16a34a", "#f97316"], // Visual palette
        }]
      }
    });
  </script>
{% endblock %}
Expected behaviour: Dashboard renders a bar chart showing domain counts using Chart.js.

Step 3: Run and Test
Launch the server with python.manage.py runserver (typo? Should be python). Wait correct command python manage.py runserver and refresh http://127.0.0.1:8000/dashboard/.

Step 4: Expected Output
A bar chart with three bars appears under the welcome text, colored blue, green, and orange.