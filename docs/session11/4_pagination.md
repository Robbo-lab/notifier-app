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
