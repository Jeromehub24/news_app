"""Regression tests for account dashboards, login, and logout flows."""

from django.test import TestCase
from django.urls import reverse

from .constants import Roles
from .models import CustomUser


class LogoutViewTests(TestCase):
    """Verify that the custom logout flow is secure and usable."""

    def setUp(self):
        """Create a reader account used by the logout-related tests."""
        self.user = CustomUser.objects.create_user(
            username="reader1",
            password="password123",
            role=Roles.READER,
        )

    def test_dashboard_renders_logout_as_post_form(self):
        """The dashboard should render logout as a POST form instead of a link."""
        self.client.force_login(self.user)

        response = self.client.get(reverse("accounts:dashboard"))

        self.assertContains(
            response,
            f'action="{reverse("accounts:logout")}"',
        )
        self.assertContains(response, 'method="post"', count=1)

    def test_logout_post_ends_the_session(self):
        """Posting to the logout endpoint should end the authenticated session."""
        self.client.force_login(self.user)

        response = self.client.post(reverse("accounts:logout"))

        self.assertRedirects(response, reverse("core:home"))
        dashboard_response = self.client.get(reverse("accounts:dashboard"))
        self.assertEqual(dashboard_response.status_code, 302)
