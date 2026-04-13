"""Regression tests for publisher workflows and editorial permissions."""

from django.test import TestCase
from django.urls import reverse

from accounts.constants import Roles
from accounts.models import CustomUser

from .models import Article, Newsletter, Publisher


class PublisherWorkflowTests(TestCase):
    """Verify publisher creation and membership flows for newsroom users."""

    def setUp(self):
        """Create editor and journalist accounts used by workflow tests."""
        self.editor = CustomUser.objects.create_user(
            username="editor1",
            password="password123",
            role=Roles.EDITOR,
        )
        self.journalist = CustomUser.objects.create_user(
            username="journalist1",
            password="password123",
            role=Roles.JOURNALIST,
        )

    def test_editor_can_create_publisher_and_is_added_to_it(self):
        """The publisher creator should automatically join as an editor."""
        self.client.force_login(self.editor)

        response = self.client.post(
            reverse("core:publisher-create"),
            {
                "name": "Daily Planet",
                "description": "Metropolis newsroom",
            },
        )

        self.assertRedirects(response, reverse("core:publisher-list"))
        publisher = Publisher.objects.get(name="Daily Planet")
        self.assertTrue(publisher.editors.filter(pk=self.editor.pk).exists())

    def test_journalist_can_join_a_publisher(self):
        """Journalists should be able to join existing publishers."""
        publisher = Publisher.objects.create(name="Bugle")
        self.client.force_login(self.journalist)

        response = self.client.post(
            reverse("core:publisher-membership", args=[publisher.pk]),
            {"action": "join"},
        )

        self.assertRedirects(response, reverse("core:publisher-list"))
        self.assertTrue(
            publisher.journalists.filter(pk=self.journalist.pk).exists()
        )


class EditorialPermissionsTests(TestCase):
    """Verify that editors can manage content created by journalists."""

    def setUp(self):
        """Create newsroom fixtures used by the editorial permission tests."""
        self.editor = CustomUser.objects.create_user(
            username="editor2",
            password="password123",
            role=Roles.EDITOR,
        )
        self.journalist = CustomUser.objects.create_user(
            username="journalist2",
            password="password123",
            role=Roles.JOURNALIST,
        )
        self.publisher = Publisher.objects.create(name="Morning Ledger")
        self.article = Article.objects.create(
            author=self.journalist,
            publisher=self.publisher,
            title="Original title",
            summary="Short summary",
            content="Original article body",
        )
        self.newsletter = Newsletter.objects.create(
            author=self.journalist,
            publisher=self.publisher,
            subject="Original subject",
            body="Original newsletter body",
        )

    def test_editor_can_update_another_users_article(self):
        """Editors should be able to edit articles created by journalists."""
        self.client.force_login(self.editor)

        response = self.client.post(
            reverse("core:article-update", args=[self.article.pk]),
            {
                "publisher": self.publisher.pk,
                "title": "Edited title",
                "summary": "Updated summary",
                "content": "Updated article body",
            },
        )

        self.assertRedirects(
            response,
            reverse("core:article-detail", args=[self.article.pk]),
        )
        self.article.refresh_from_db()
        self.assertEqual(self.article.title, "Edited title")

    def test_editor_can_delete_another_users_article(self):
        """Editors should be able to delete articles they did not author."""
        self.client.force_login(self.editor)

        response = self.client.post(
            reverse("core:article-delete", args=[self.article.pk])
        )

        self.assertRedirects(response, reverse("core:article-list"))
        self.assertFalse(Article.objects.filter(pk=self.article.pk).exists())

    def test_editor_can_update_another_users_newsletter(self):
        """Editors should be able to update newsletter drafts by journalists."""
        self.client.force_login(self.editor)

        response = self.client.post(
            reverse("core:newsletter-update", args=[self.newsletter.pk]),
            {
                "publisher": self.publisher.pk,
                "subject": "Edited subject",
                "body": "Updated newsletter body",
            },
        )

        self.assertRedirects(response, reverse("core:newsletter-list"))
        self.newsletter.refresh_from_db()
        self.assertEqual(self.newsletter.subject, "Edited subject")

    def test_editor_can_delete_another_users_newsletter(self):
        """Editors should be able to delete newsletter drafts by journalists."""
        self.client.force_login(self.editor)

        response = self.client.post(
            reverse("core:newsletter-delete", args=[self.newsletter.pk])
        )

        self.assertRedirects(response, reverse("core:newsletter-list"))
        self.assertFalse(
            Newsletter.objects.filter(pk=self.newsletter.pk).exists()
        )
