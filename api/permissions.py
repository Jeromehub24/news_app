"""
Custom API permissions.

This file is where role-aware API access rules should live.
"""

from rest_framework import permissions


class IsAuthenticatedNewsUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)
