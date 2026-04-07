"""
Top-level URL router for the News Application project.

What this file is for:
- This file is the map that sends incoming requests to the correct app.
- It does not hold the business logic itself. Its job is routing.

How this file connects to the rest of the project:
- `/accounts/` goes to `accounts/urls.py`
- `/api/` goes to `api/urls.py`
- The public site pages go to `core/urls.py`
"""

from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("core.urls")),
    path("accounts/", include("accounts.urls")),
    path("api/", include("api.urls")),
]
