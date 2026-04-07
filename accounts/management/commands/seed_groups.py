from django.core.management.base import BaseCommand

from accounts.services import ensure_role_groups_exist


class Command(BaseCommand):
    help = "Create the baseline Reader, Editor, and Journalist groups."

    def handle(self, *args, **options):
        ensure_role_groups_exist()
        self.stdout.write(self.style.SUCCESS("Role groups are ready."))
