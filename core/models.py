"""Core data models for publishers, articles, and newsletters."""

from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify


def build_unique_slug(model_class, value, instance=None):
    """Generate a slug that is unique for the given model and value."""
    base_slug = slugify(value) or "item"
    slug = base_slug
    counter = 2

    # Keep the current record eligible so edits can reuse the same slug.
    while (
        model_class.objects.filter(slug=slug)
        .exclude(pk=getattr(instance, "pk", None))
        .exists()
    ):
        slug = f"{base_slug}-{counter}"
        counter += 1

    return slug


class Publisher(models.Model):
    """Represent a publisher that editors and journalists can join."""

    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    description = models.TextField(blank=True)
    editors = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        blank=True,
        related_name="editor_publications",
        help_text="Editors who oversee this publication.",
    )
    journalists = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        blank=True,
        related_name="journalist_publications",
        help_text="Journalists who publish under this publication.",
    )

    def save(self, *args, **kwargs):
        """Populate the slug automatically before saving a publisher."""
        if not self.slug:
            self.slug = build_unique_slug(Publisher, self.name, self)
        super().save(*args, **kwargs)

    def __str__(self):
        """Return the publisher name for templates and admin displays."""
        return self.name


class Article(models.Model):
    """Store an article draft or approved publication for the newsroom."""

    publisher = models.ForeignKey(
        Publisher,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="articles",
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="articles",
    )
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    summary = models.TextField(blank=True)
    content = models.TextField()
    approved = models.BooleanField(default=False)
    approved_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        """Generate missing slugs and stamp publish dates after approval."""
        if not self.slug:
            self.slug = build_unique_slug(Article, self.title, self)
        if self.approved and self.published_at is None:
            self.published_at = timezone.now()
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        """Return the canonical detail page for the current article."""
        return reverse("core:article-detail", kwargs={"pk": self.pk})

    def __str__(self):
        """Return the article title for admin, templates, and serializers."""
        return self.title


class Newsletter(models.Model):
    """Store newsletter content drafted by newsroom users."""

    publisher = models.ForeignKey(
        Publisher,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="newsletters",
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="newsletters",
    )
    subject = models.CharField(max_length=255)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        """Return the newsletter listing page after create or update actions."""
        return reverse("core:newsletter-list")

    def __str__(self):
        """Return the newsletter subject for display purposes."""
        return self.subject
