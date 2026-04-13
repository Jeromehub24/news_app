"""Signal handlers that keep custom users aligned with Django groups."""

from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import CustomUser
from .services import sync_user_role_group


@receiver(post_save, sender=CustomUser)
def keep_role_group_in_sync(sender, instance, **kwargs):
    """Refresh the saved user's Django group membership after each save."""
    sync_user_role_group(instance)
