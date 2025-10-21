<!-- activity_basic_view.md -->
Activity 1: Basic View and Template Rendering
Learning Objective
Render a template with context data using Django’s render() shortcut.

Step 1: File and Context
Add a dashboard view to the existing notifications app so students land on a welcome page fed by dynamic context.

Step 2: Add the Code
# notifications/views.py
from django.shortcuts import render  # Import render helper

def dashboard(request):
    # Build the context dictionary that template will consume
    context = {
        "page_title": "Notifier Dashboard",  # Title shown in the browser tab
        "welcome_message": "Welcome to the notifier control panel!",  # Hero text
        "active_alerts": ["Server Load High", "Email Queue Delayed"],  # Sample list data
    }
    # Render the HTML template with the context for this request
    return render(request, "notifications/dashboard.html", context)
Expected behaviour: Django will look for notifications/dashboard.html and pass the context variables to it when /dashboard/ is requested.

# notifications/urls.py
from django.urls import path  # URL dispatcher helper
from . import views  # Import the views module from the same app

urlpatterns = [
    path("dashboard/", views.dashboard, name="dashboard"),  # Map URL to the new view
]
Expected behaviour: Visiting /dashboard/ now routes to the dashboard view without touching existing patterns.

<!-- templates/notifications/dashboard.html -->
{% extends "base.html" %} <!-- Reuse global layout if available -->

{% block content %}
  <section>
    <h1>{{ page_title }}</h1> <!-- Display the title from context -->
    <p>{{ welcome_message }}</p> <!-- Show the welcome text -->
    <ul>
      {% for alert in active_alerts %}
        <li>{{ alert }}</li> <!-- Loop through alerts -->
      {% empty %}
        <li>No active alerts right now.</li> <!-- Fallback when list is empty -->
      {% endfor %}
    </ul>
  </section>
{% endblock %}
Expected behaviour: The template displays the title, message, and a bullet list populated from the context.

Step 3: Run and Test
Run python manage.py runserver and open http://127.0.0.1:8000/dashboard/.

Step 4: Expected Output
Browser shows the dashboard heading, welcome text, and the two sample alerts rendered as list items.

Reflection
What did you notice about how context variables map into template placeholders?
✅ Step complete – visit http://127.0.0.1:8000/dashboard/

<!-- activity_template_inheritance.md -->
Activity 2: Template Inheritance with base.html
Learning Objective
Use Django template inheritance to keep page structure DRY.

Step 1: File and Context
Upgrade the dashboard to extend from a new base.html layout so child templates share the same frame.

Step 2: Add the Code
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
Expected behaviour: Any template extending base.html gets the shared header, nav, and footer automatically.

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
Expected behaviour: Content is injected into the base template while keeping the full layout consistent.

Step 3: Run and Test
Execute python manage.py runserver and refresh http://127.0.0.1:8000/dashboard/.

Step 4: Expected Output
Page now shows the global header, navigation, and footer surrounding the dashboard content.

Reflection
How does changing base.html affect all child templates instantly?
✅ Step complete – visit http://127.0.0.1:8000/dashboard/

<!-- activity_forms_validation.md -->
Activity 3: Creating and Validating a Django Form
Learning Objective
Collect user input with a custom forms.Form and validate it using clean_<field>.

Step 1: File and Context
Allow operators to request a notification test email using a form view in the notifications app.

Step 2: Add the Code
# notifications/forms.py
from django import forms  # Import Django forms toolkit

class TestEmailForm(forms.Form):
    recipient = forms.EmailField(label="Recipient email")  # Built-in email validation
    subject = forms.CharField(max_length=120, label="Subject")  # Limit to 120 chars
    message = forms.CharField(widget=forms.Textarea, label="Message")  # Multiline message

    def clean_subject(self):
        # Obtain the cleaned subject value
        subject = self.cleaned_data["subject"]
        # Enforce that the subject contains the word "Test" for clarity
        if "test" not in subject.lower():
            raise forms.ValidationError("Subject must include the word 'Test'.")
        # Return the validated subject
        return subject
Expected behaviour: Form raises a validation error if the subject does not contain “Test”.

# notifications/views.py
from django.contrib import messages  # For success notification
from .forms import TestEmailForm  # Import the new form

def request_test_email(request):
    # Instantiate the form with POST data or empty for GET
    form = TestEmailForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        # Simulate sending an email here (integration point)
        messages.success(request, "Test email queued successfully!")  # Feedback banner
        # Redisplay a fresh form after processing
        form = TestEmailForm()
    # Render template with the form context
    return render(request, "notifications/request_test_email.html", {"form": form})
Expected behaviour: On valid POST, the page resets the form and shows a success message using Django’s messages framework.

# notifications/urls.py
urlpatterns = [
    path("dashboard/", views.dashboard, name="dashboard"),  # Existing pattern
    path("request-test-email/", views.request_test_email, name="request_test_email"),  # New form page
]
Expected behaviour: URL routing now exposes /request-test-email/ without altering previous routes.

<!-- templates/notifications/request_test_email.html -->
{% extends "base.html" %}

{% block title %}Request Test Email{% endblock %}

{% block content %}
  <h2>Request a Notification Test Email</h2>
  {% if messages %}
    <ul>
      {% for message in messages %}
        <li>{{ message }}</li> <!-- Display success feedback -->
      {% endfor %}
    </ul>
  {% endif %}
  <form method="post">
    {% csrf_token %} <!-- Protect against CSRF -->
    {{ form.as_p }} <!-- Render form fields with labels -->
    <button type="submit">Send Test Email</button> <!-- Submit action -->
  </form>
{% endblock %}
Expected behaviour: Form displays with fields and shows a success banner when validation passes.

Step 3: Run and Test
Start the server with python manage.py runserver and submit the form at http://127.0.0.1:8000/request-test-email/.

Step 4: Expected Output
If “Test” appears in the subject, a success message is shown; otherwise, inline validation errors appear.

Reflection
How does the clean_subject method help enforce business rules without hitting the database?
✅ Step complete – visit http://127.0.0.1:8000/request-test-email/

<!-- activity_csv_upload.md -->
Activity 4: Handling CSV Uploads with Pandas Validation
Learning Objective
Validate uploaded CSV files using Pandas before processing them.

Step 1: File and Context
Enable operators to upload notification recipients via CSV in the alerts app, validating schema before saving.

Step 2: Add the Code
# alerts/forms.py
from django import forms  # Form helpers

class RecipientUploadForm(forms.Form):
    csv_file = forms.FileField(label="Recipient CSV")  # File input field
Expected behaviour: Simple form collects CSV file uploads.

# alerts/views.py
import pandas as pd  # Data validation helper
from django.contrib import messages  # To show error feedback
from django.shortcuts import redirect, render  # To render templates and redirect
from .forms import RecipientUploadForm  # Import upload form

REQUIRED_COLUMNS = {"email", "first_name", "last_name"}  # Expected CSV schema

def upload_recipients(request):
    # Instantiate form with request data and files
    form = RecipientUploadForm(request.POST or None, request.FILES or None)
    if request.method == "POST" and form.is_valid():
        # Read uploaded file into DataFrame
        df = pd.read_csv(request.FILES["csv_file"])
        # Calculate missing columns using set difference
        missing = REQUIRED_COLUMNS - set(df.columns.str.lower())
        if missing:
            # Surface validation error without storing file
            messages.error(request, f"Missing columns: {', '.join(sorted(missing))}")
        else:
            # TODO: Replace with model bulk_create or other persistence logic
            messages.success(request, f"Uploaded {len(df)} recipients successfully.")
            return redirect("alerts:preview_recipients")  # Proceed to preview step
    # Render template with current form state
    return render(request, "alerts/upload_recipients.html", {"form": form})
Expected behaviour: Upload rejects files missing required columns and flashes descriptive messages.

# alerts/urls.py
from django.urls import path  # URL helper
from . import views  # Import view module

app_name = "alerts"  # Namespacing
urlpatterns = [
    path("upload/", views.upload_recipients, name="upload_recipients"),  # New upload route
]
Expected behaviour: Namespaced URL /alerts/upload/ routes to the uploader.

<!-- templates/alerts/upload_recipients.html -->
{% extends "base.html" %}

{% block title %}Upload Recipients{% endblock %}

{% block content %}
  <h2>Upload Recipients (CSV)</h2>
  <p>Expected columns: email, first_name, last_name</p> <!-- Explain schema -->
  {% if messages %}
    <ul>
      {% for message in messages %}
        <li>{{ message }}</li> <!-- Feedback for success or errors -->
      {% endfor %}
    </ul>
  {% endif %}
  <form method="post" enctype="multipart/form-data">
    {% csrf_token %}
    {{ form.as_p }} <!-- Render file field -->
    <button type="submit">Validate File</button>
  </form>
{% endblock %}
Expected behaviour: Page displays file uploader and any validation errors from Pandas.

Step 3: Run and Test
Upload a CSV using python manage.py runserver then visit http://127.0.0.1:8000/alerts/upload/.

Step 4: Expected Output
Valid CSVs trigger a success message and redirect; incorrect schemas stay on the page with missing column details.

Reflection
What checks would you add if duplicate emails are not allowed?
✅ Step complete – visit http://127.0.0.1:8000/alerts/upload/

<!-- activity_preview_pagination.md -->
Activity 5: Previewing Uploaded Data with Pagination
Learning Objective
Display validated CSV data with Django’s Paginator for manageable previews.

Step 1: File and Context
After successful upload, show a preview page listing recipients with pagination inside the alerts app.

Step 2: Add the Code
# alerts/views.py
from django.core.paginator import Paginator  # Pagination utility
from django.http import HttpRequest  # Type hint (optional)
from django.utils.safestring import mark_safe  # For safe HTML messages

def preview_recipients(request: HttpRequest):
    # Placeholder data until persistence is added; replace with session or DB query
    sample_data = [
        {"email": f"user{i}@example.com", "first_name": f"First{i}", "last_name": f"Last{i}"}
        for i in range(1, 51)
    ]
    # Instantiate paginator with 10 items per page
    paginator = Paginator(sample_data, 10)
    # Get requested page or default to 1
    page_number = request.GET.get("page", 1)
    page_obj = paginator.get_page(page_number)
    # Provide page object to template for iteration
    return render(request, "alerts/preview_recipients.html", {"page_obj": page_obj})
Expected behaviour: View builds a paginated list of sample recipients and passes the current page to the template safely.

# alerts/urls.py
urlpatterns = [
    path("upload/", views.upload_recipients, name="upload_recipients"),
    path("preview/", views.preview_recipients, name="preview_recipients"),  # New preview route
]
Expected behaviour: /alerts/preview/ now maps to the preview view.

<!-- templates/alerts/preview_recipients.html -->
{% extends "base.html" %}

{% block title %}Recipient Preview{% endblock %}

{% block content %}
  <h2>Preview Recipients</h2>
  <table>
    <thead>
      <tr>
        <th>Email</th>
        <th>First Name</th>
        <th>Last Name</th>
      </tr>
    </thead>
    <tbody>
      {% for row in page_obj.object_list %}
        <tr>
          <td>{{ row.email }}</td>
          <td>{{ row.first_name }}</td>
          <td>{{ row.last_name }}</td>
        </tr>
      {% empty %}
        <tr>
          <td colspan="3">No data available.</td>
        </tr>
      {% endfor %}
    </tbody>
  </table>

  <nav>
    {% if page_obj.has_previous %}
      <a href="?page={{ page_obj.previous_page_number }}">Previous</a> <!-- Link to prior page -->
    {% endif %}
    <span>Page {{ page_obj.number }} of {{ page_obj.paginator.num_pages }}</span> <!-- Show position -->
    {% if page_obj.has_next %}
      <a href="?page={{ page_obj.next_page_number }}">Next</a> <!-- Link to next page -->
    {% endif %}
  </nav>
{% endblock %}
Expected behaviour: Table lists ten recipients per page with navigation links.

Step 3: Run and Test
Start the server (python manage.py runserver) then open http://127.0.0.1:8000/alerts/preview/.

Step 4: Expected Output
Table displays sample recipients with working previous/next links reflecting pagination.

Reflection
Where would you persist the uploaded rows so the preview shows real data?
✅ Step complete – visit http://127.0.0.1:8000/alerts/preview/

<!-- activity_chartjs_visualization.md -->
Activity 6: Rendering a Chart.js Visualization
Learning Objective
Display aggregated recipient stats using Chart.js fed from Django context data.

Step 1: File and Context
Visualize the count of recipients by domain on the dashboard using Chart.js.

Step 2: Add the Code
# notifications/views.py
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

Reflection
How would you compute the domain_counts dynamically from uploaded data?
✅ Step complete – visit http://127.0.0.1:8000/dashboard/

<!-- activity_plotly_visualization.md -->
Activity 7: Rendering a Plotly Chart with JSON-Safe Variables
Learning Objective
Embed a Plotly chart using json_script to safely provide data from Django views.

Step 1: File and Context
Add a route to show delivery success rates using an interactive Plotly pie chart.

Step 2: Add the Code
# notifications/views.py
import json  # Standard library for serialization
from django.utils.safestring import mark_safe  # For safe script tag injection

def delivery_stats(request):
    # Build dictionary representing chart data
    chart_data = {
        "labels": ["Delivered", "Bounced", "Deferred"],
        "values": [180, 15, 5],
    }
    # Render template with serialized JSON for Plotly
    return render(
        request,
        "notifications/delivery_stats.html",
        {"chart_data_json": json.dumps(chart_data)},  # Pass as JSON string
    )
Expected behaviour: View prepares JSON for the template without exposing Python objects.

# notifications/urls.py
urlpatterns = [
    path("dashboard/", views.dashboard, name="dashboard"),
    path("request-test-email/", views.request_test_email, name="request_test_email"),
    path("delivery-stats/", views.delivery_stats, name="delivery_stats"),  # New stats page
]
Expected behaviour: URL /delivery-stats/ now points to the new view.

<!-- templates/notifications/delivery_stats.html -->
{% extends "base.html" %}

{% block title %}Delivery Stats{% endblock %}

{% block content %}
  <h2>Delivery Outcomes</h2>
  <div id="delivery-chart"></div> <!-- Placeholder for Plotly graph -->
  {{ chart_data_json|json_script:"delivery-data" }} <!-- Serialize safely -->
  <script src="https://cdn.plot.ly/plotly-latest.min.js"></script> <!-- Plotly CDN -->
  <script>
    // Parse the JSON data safely using Django's helper
    const data = JSON.parse(document.getElementById("delivery-data").textContent);
    // Build Plotly dataset
    const plotted = [{
      type: "pie", // Pie chart
      labels: data.labels, // Slice labels
      values: data.values, // Slice values
      textinfo: "label+percent", // Show label and percent
    }];
    // Render chart into the target div
    Plotly.newPlot("delivery-chart", plotted);
  </script>
{% endblock %}
Expected behaviour: Page renders a Plotly pie chart showing delivery ratios using sanitized JSON.

Step 3: Run and Test
Use python manage.py runserver and navigate to http://127.0.0.1:8000/delivery-stats/.

Step 4: Expected Output
Interactive pie chart appears with sections for Delivered, Bounced, and Deferred emails.

Reflection
When might you stream chart data via an API instead of embedding JSON?
✅ Step complete – visit http://127.0.0.1:8000/delivery-stats/

<!-- activity_auto_escaping.md -->
Activity 8: Django Auto-Escaping and |safe
Learning Objective
Demonstrate Django’s auto-escaping feature and highlight when to use |safe.

Step 1: File and Context
Show how user-supplied HTML is escaped by default on the preview page, with an opt-in safe rendering for trusted snippets.

Step 2: Add the Code
# alerts/views.py
def preview_recipients(request):
    sample_data = [
        {"email": "user@example.com", "first_name": "First", "last_name": "Last"},
    ]
    # Emulate HTML passed in from a trusted admin note
    trusted_html = "<strong>Reminder:</strong> Review bounced addresses today."
    context = {
        "page_obj": Paginator(sample_data, 10).get_page(1),
        "trusted_html": trusted_html,  # Trusted HTML fragment
    }
    return render(request, "alerts/preview_recipients.html", context)
Expected behaviour: Context includes HTML that should be shown differently depending on escaping.

<!-- templates/alerts/preview_recipients.html -->
{% extends "base.html" %}

{% block title %}Recipient Preview{% endblock %}

{% block content %}
  <h2>Preview Recipients</h2>
  <p>Default auto-escaped note: {{ trusted_html }}</p> <!-- Displays literal tags -->
  <p>Trusted note with safe filter: {{ trusted_html|safe }}</p> <!-- Renders bold text -->
  <!-- Existing table markup remains unchanged -->
{% endblock %}
Expected behaviour: First paragraph shows angle brackets, second renders bold text via |safe.

Step 3: Run and Test
Run python manage.py runserver and view http://127.0.0.1:8000/alerts/preview/.

Step 4: Expected Output
Two notes display: one with literal <strong> tags, the other with bold text.

Reflection
How do you decide when it is safe to apply the |safe filter?
✅ Step complete – visit http://127.0.0.1:8000/alerts/preview/

<!-- activity_streamlit_alternative.md -->
Activity 10: Streamlit Dashboard Alternative
Learning Objective
Provide a quick Streamlit dashboard that mirrors Django metrics for rapid prototyping.

Step 1: File and Context
Build a streamlit_app.py in the project root to visualize data without touching the Django runtime.

Step 2: Add the Code
# streamlit_app.py
import pandas as pd  # Data manipulation helper
import streamlit as st  # Streamlit framework

st.set_page_config(page_title="Notifier Live Stats")  # Configure Streamlit page
st.title("Notifier Dashboard (Streamlit Prototype)")  # Main heading

# Simulate pulling data from Django model or service
data = pd.DataFrame([
    {"email": "user1@example.com", "status": "Delivered"},
    {"email": "user2@example.com", "status": "Bounced"},
])

st.write("Recent notification statuses:", data)  # Display table
status_counts = data["status"].value_counts()  # Aggregate by status
st.bar_chart(status_counts)  # Quick chart visualization
Expected behaviour: Running the Streamlit script opens a web app showing the table and bar chart.

Step 3: Run and Test
From the project root run streamlit run streamlit_app.py and open the served URL.

Step 4: Expected Output
Streamlit page displays the sample DataFrame and a bar chart with Delivered vs Bounced counts.

Reflection
Where could Streamlit fit into your workflow alongside Django?
✅ Step complete – visit http://127.0.0.1:8501/

<!-- activity_escaping_sanitization.md -->
Activity 11: Escaping and Sanitization with mark_safe and bleach
Learning Objective
Safely allow limited HTML while sanitizing untrusted input using bleach.

Step 1: File and Context
Allow staff to add admin notes with limited formatting to display on the dashboard without exposing XSS risks.

Step 2: Add the Code
# notifications/utils.py
import bleach  # Sanitization library
from django.utils.safestring import mark_safe  # Mark sanitized HTML as safe

ALLOWED_TAGS = ["strong", "em", "a", "ul", "li"]  # HTML tags we trust
ALLOWED_ATTRIBUTES = {"a": ["href", "title", "target"]}  # Allowed link attributes

def sanitize_note(raw_html: str) -> str:
    # Clean the input HTML using bleach
    cleaned = bleach.clean(raw_html, tags=ALLOWED_TAGS, attributes=ALLOWED_ATTRIBUTES)
    # Mark the sanitized HTML as safe for template rendering
    return mark_safe(cleaned)
Expected behaviour: Function removes disallowed tags and returns marked-safe HTML.

# notifications/views.py
from .utils import sanitize_note  # Import sanitizer

def dashboard(request):
    raw_note = "<script>alert('xss')</script><strong>System stable.</strong>"  # Simulated input
    context = {
        "page_title": "Notifier Dashboard",
        "welcome_message": "Welcome to the notifier control panel!",
        "active_alerts": ["Server Load High", "Email Queue Delayed"],
        "domain_labels": ["example.com", "school.edu", "vendor.net"],
        "domain_counts": [25, 10, 8],
        "admin_note": sanitize_note(raw_note),  # Store sanitized HTML
    }
    return render(request, "notifications/dashboard.html", context)
Expected behaviour: Dashboard context now contains sanitized admin note that strips scripts but keeps bold text.

<!-- templates/notifications/dashboard.html -->
{% extends "base.html" %}

{% block content %}
  <section>
    <h2>{{ page_title }}</h2>
    <p>{{ welcome_message }}</p>
    <div class="admin-note">
      {{ admin_note }} <!-- Displays sanitized HTML without re-escaping -->
    </div>
    <!-- Existing chart canvas etc. remains -->
  </section>
{% endblock %}
Expected behaviour: Template renders the note safely with <strong> preserved and <script> removed.

Step 3: Run and Test
Install bleach if needed (pip install bleach) then run python manage.py runserver and browse to http://127.0.0.1:8000/dashboard/.

Step 4: Expected Output
Page shows “System stable.” in bold within the admin note area without executing any script.

Reflection
How would you store the sanitized note so it isn’t re-cleaned on every request?
✅ Step complete – visit http://127.0.0.1:8000/dashboard/

<!-- activity_combined_workflow.md -->
Activity 12: End-to-End Workflow – Upload → Validate → Preview → Chart
Learning Objective
Link the CSV upload, validation, preview, and visualization into one cohesive workflow.

Step 1: File and Context
Extend the alerts workflow so a successful CSV upload redirects through preview and finally updates dashboard charts.

Step 2: Add the Code
# alerts/views.py
from django.urls import reverse  # For constructing redirect URL
from django.utils import timezone  # Timestamp storage

UPLOADED_DATA_SESSION_KEY = "uploaded_recipients"  # Session key for storage

def upload_recipients(request):
    form = RecipientUploadForm(request.POST or None, request.FILES or None)
    if request.method == "POST" and form.is_valid():
        df = pd.read_csv(request.FILES["csv_file"])
        missing = REQUIRED_COLUMNS - set(df.columns.str.lower())
        if missing:
            messages.error(request, f"Missing columns: {', '.join(sorted(missing))}")
        else:
            # Store sanitized records in session for preview
            request.session[UPLOADED_DATA_SESSION_KEY] = df.to_dict(orient="records")
            request.session["upload_timestamp"] = timezone.now().isoformat()
            messages.success(request, f"Uploaded {len(df)} recipients successfully.")
            return redirect("alerts:preview_recipients")  # Step into preview
    return render(request, "alerts/upload_recipients.html", {"form": form})

def preview_recipients(request):
    # Retrieve data from session or fallback to empty list
    records = request.session.get(UPLOADED_DATA_SESSION_KEY, [])
    paginator = Paginator(records, 10)
    page_obj = paginator.get_page(request.GET.get("page", 1))
    return render(
        request,
        "alerts/preview_recipients.html",
        {
            "page_obj": page_obj,
            "uploaded_total": len(records),
            "upload_timestamp": request.session.get("upload_timestamp"),
        },
    )
Expected behaviour: Valid uploads are stored in session, preview loads actual uploaded data.

# notifications/views.py
from collections import Counter  # To aggregate counts

def dashboard(request):
    # Pull uploaded recipients from session if available
    records = request.session.get("uploaded_recipients", [])
    domains = [record["email"].split("@")[-1] for record in records if "email" in record]
    counts = Counter(domains)
    context = {
        "page_title": "Notifier Dashboard",
        "welcome_message": "Welcome to the notifier control panel!",
        "active_alerts": ["Server Load High", "Email Queue Delayed"],
        "domain_labels": list(counts.keys()) or ["example.com"],
        "domain_counts": list(counts.values()) or [0],
        "recent_upload_total": len(records),
    }
    return render(request, "notifications/dashboard.html", context)
Expected behaviour: Dashboard chart updates based on session data so the chart reflects the latest upload.

<!-- templates/notifications/dashboard.html -->
{% extends "base.html" %}

{% block content %}
  <section>
    <h2>{{ page_title }}</h2>
    <p>{{ welcome_message }}</p>
    <p>Total recipients in last upload: {{ recent_upload_total }}</p> <!-- Show summary -->
    <canvas id="domainChart" width="400" height="200"></canvas>
  </section>
  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
  <script>
    const ctx = document.getElementById("domainChart");
    new Chart(ctx, {
      type: "bar",
      data: {
        labels: {{ domain_labels|safe }},
        datasets: [{
          label: "Recipients per Domain",
          data: {{ domain_counts|safe }},
          backgroundColor: "#2563eb",
        }]
      }
    });
  </script>
{% endblock %}
Expected behaviour: Chart dynamically reflects domains from the most recent upload with count summary above.

<!-- templates/alerts/preview_recipients.html -->
{% extends "base.html" %}

{% block content %}
  <h2>Preview Recipients</h2>
  <p>Total uploaded: {{ uploaded_total }}</p> <!-- Show total count -->
  <p>Uploaded at: {{ upload_timestamp }}</p> <!-- Timestamp context -->
  <!-- Existing table and pagination remain intact -->
{% endblock %}
Expected behaviour: Preview page displays total rows and upload time alongside the table.

Step 3: Run and Test
Start server: python manage.py runserver.
Upload a CSV at http://127.0.0.1:8000/alerts/upload/.
Inspect preview at http://127.0.0.1:8000/alerts/preview/.
Return to dashboard http://127.0.0.1:8000/dashboard/.
Step 4: Expected Output
Flow moves from upload (success message) → preview (with real rows and totals) → dashboard (chart updated with domain counts).

Reflection
How would you persist recipient data so it survives server restarts?
✅ Step complete – visit http://127.0.0.1:8000/dashboard/

what is the url path for the main urls.py file for alerts


notifier/alerts/urls.py