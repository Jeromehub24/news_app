"""
Serializers translate Django model instances into JSON-friendly data.
"""

from rest_framework import serializers

from core.models import Article, Newsletter, Publisher


class PublisherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publisher
        fields = ("id", "name", "slug", "description")


class ArticleSerializer(serializers.ModelSerializer):
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
    publisher = serializers.StringRelatedField()
    author = serializers.StringRelatedField()

    class Meta:
        model = Newsletter
        fields = ("id", "subject", "body", "publisher", "author", "created_at")
