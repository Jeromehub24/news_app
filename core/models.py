from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify


def build_unique_slug(model_class, value, instance=None):
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
        if not self.slug:
            self.slug = build_unique_slug(Publisher, self.name, self)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Article(models.Model):
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
        if not self.slug:
            self.slug = build_unique_slug(Article, self.title, self)
        if self.approved and self.published_at is None:
            self.published_at = timezone.now()
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("core:article-detail", kwargs={"pk": self.pk})

    def __str__(self):
        return self.title


class Newsletter(models.Model):
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
        return reverse("core:newsletter-list")

    def __str__(self):
        return self.subject
