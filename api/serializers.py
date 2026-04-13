"""Serializers that expose newsroom models through the REST API."""

from rest_framework import serializers

from core.models import Article, Newsletter, Publisher


class PublisherSerializer(serializers.ModelSerializer):
    """Serialize publisher details for list and detail API responses."""

    class Meta:
        model = Publisher
        fields = ("id", "name", "slug", "description")


class ArticleSerializer(serializers.ModelSerializer):
    """Serialize approved articles with human-readable author metadata."""

    publisher = serializers.StringRelatedField()
    author = serializers.StringRelatedField()

    class Meta:
        model = Article
        fields = (
            "id",
            "title",
            "slug",
            "summary",
            "content",
            "approved",
            "published_at",
            "publisher",
            "author",
        )


class NewsletterSerializer(serializers.ModelSerializer):
    """Serialize newsletter drafts and published newsletter information."""

    publisher = serializers.StringRelatedField()
    author = serializers.StringRelatedField()

    class Meta:
        model = Newsletter
        fields = ("id", "subject", "body", "publisher", "author", "created_at")
