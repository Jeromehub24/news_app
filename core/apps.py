"""Application configuration for the core publishing app."""

from django.apps import AppConfig


class CoreConfig(AppConfig):
    """Register the core app with Django."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "core"
