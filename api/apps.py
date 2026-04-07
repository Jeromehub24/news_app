"""
App configuration for the API layer.

Why this app exists:
- The capstone requires a RESTful API.
"""

from django.apps import AppConfig


class ApiConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "api"
