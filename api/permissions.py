"""Custom permission classes for News App API endpoints."""

from rest_framework import permissions


class IsAuthenticatedNewsUser(permissions.BasePermission):
    """Allow API access only for authenticated Django users."""

    def has_permission(self, request, view):
        """Return ``True`` when the request is made by a signed-in user."""
        return bool(request.user and request.user.is_authenticated)
