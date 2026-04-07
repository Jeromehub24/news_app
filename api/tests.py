"""
Tests for the REST API.

Suggested checklist:
- Authenticated clients can reach the feed endpoint.
- Feed returns approved articles from subscribed publishers.
- Feed returns approved articles from subscribed journalists.
- Unauthenticated requests are rejected.
"""

from rest_framework.test import APITestCase


class ApiScaffoldTests(APITestCase):
    pass
