"""Application configuration for the accounts app."""

from django.apps import AppConfig


class AccountsConfig(AppConfig):
    """Register startup behavior for account-related signals."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "accounts"

    def ready(self):
        """Import signal handlers after Django finishes loading apps."""
        from . import signals  # noqa: F401
