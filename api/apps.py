"""Application configuration for the API app."""

from django.apps import AppConfig


class ApiConfig(AppConfig):
    """Register the REST API application with Django."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "api"
