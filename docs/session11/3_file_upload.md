<!-- activity_csv_upload.md -->

Activity 4: Handling CSV Uploads with Pandas Validation
Learning Objective
Validate uploaded CSV files using Pandas before processing them.

Step 1: File and Context
Enable operators to upload notification recipients via CSV in the alerts app, validating schema before saving.

Step 2: Add the Code

# alerts/forms.py

from django import forms # Form helpers

class RecipientUploadForm(forms.Form):
csv_file = forms.FileField(label="Recipient CSV") # File input field
Expected behaviour: Simple form collects CSV file uploads.

# alerts/views.py

```python
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
```

Expected behaviour: Namespaced URL /alerts/upload/ routes to the uploader.

```html
<!-- templates/alerts/upload_recipients.html -->
{% extends "base.html" %} {% block title %}Upload Recipients{% endblock %} {%
block content %}
<h2>Upload Recipients (CSV)</h2>
<p>Expected columns: email, first_name, last_name</p>
<!-- Explain schema -->
{% if messages %}
<ul>
    {% for message in messages %}
    <li>{{ message }}</li>
    <!-- Feedback for success or errors -->
    {% endfor %}
</ul>
{% endif %}
<form method="post" enctype="multipart/form-data">
    {% csrf_token %} {{ form.as_p }}
    <!-- Render file field -->
    <button type="submit">Validate File</button>
</form>
{% endblock %}
```

Expected behaviour: Page displays file uploader and any validation errors from Pandas.

Step 3: Run and Test
Upload a CSV using python manage.py runserver then visit http://127.0.0.1:8000/alerts/upload/.

Step 4: Expected Output
Valid CSVs trigger a success message and redirect; incorrect schemas stay on the page with missing column details.
