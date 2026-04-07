from django.test import TestCase
from django.urls import reverse

from .constants import Roles
from .models import CustomUser


class LogoutViewTests(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username="reader1",
            password="password123",
            role=Roles.READER,
        )

    def test_dashboard_renders_logout_as_post_form(self):
        self.client.force_login(self.user)

        response = self.client.get(reverse("accounts:dashboard"))

        self.assertContains(
            response,
            f'action="{reverse("accounts:logout")}"',
        )
        self.assertContains(response, 'method="post"', count=1)

    def test_logout_post_ends_the_session(self):
        self.client.force_login(self.user)

        response = self.client.post(reverse("accounts:logout"))

        self.assertRedirects(response, reverse("core:home"))
        dashboard_response = self.client.get(reverse("accounts:dashboard"))
        self.assertEqual(dashboard_response.status_code, 302)
