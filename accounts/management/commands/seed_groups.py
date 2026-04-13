"""Management command for creating the default newsroom permission groups."""

from django.core.management.base import BaseCommand

from accounts.services import ensure_role_groups_exist


class Command(BaseCommand):
    """Create the baseline Django auth groups used by the application."""

    help = "Create the baseline Reader, Editor, and Journalist groups."

    def handle(self, *args, **options):
        """Seed the Reader, Editor, and Journalist groups into the database."""
        ensure_role_groups_exist()
        self.stdout.write(self.style.SUCCESS("Role groups are ready."))
