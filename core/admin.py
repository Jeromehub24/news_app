"""Admin registrations for publishers, articles, and newsletters."""

from django.contrib import admin

from .models import Article, Newsletter, Publisher


@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
    """Display publishers in the Django admin with search support."""

    list_display = ("name", "slug")
    search_fields = ("name", "slug")


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    """Expose article moderation fields in the Django admin interface."""

    list_display = ("title", "author", "publisher", "approved", "created_at")
    list_filter = ("approved", "publisher")
    search_fields = ("title", "summary", "content")
    prepopulated_fields = {"slug": ("title",)}


@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    """Configure newsletter editing and filtering in the admin site."""

    list_display = ("subject", "author", "publisher", "created_at")
    list_filter = ("publisher",)
    search_fields = ("subject", "body")
