"""Helpers for keeping Django groups aligned with application roles."""

from django.contrib.auth.models import Group

from .constants import ROLE_TO_GROUP


def ensure_role_groups_exist():
    """Create the default role groups if they do not exist yet."""
    for group_name in ROLE_TO_GROUP.values():
        Group.objects.get_or_create(name=group_name)


def sync_user_role_group(user):
    """Replace the user's tracked role group with the expected one."""
    ensure_role_groups_exist()
    valid_group_names = set(ROLE_TO_GROUP.values())
    current_groups = list(user.groups.filter(name__in=valid_group_names))
    if current_groups:
        user.groups.remove(*current_groups)
    expected_group_name = ROLE_TO_GROUP.get(user.role)
    if expected_group_name:
        user.groups.add(Group.objects.get(name=expected_group_name))
