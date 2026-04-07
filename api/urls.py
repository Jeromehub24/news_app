"""
URL routes for the REST API.
"""

from django.urls import path

from .views import PublisherListAPIView, SubscribedArticleFeedAPIView

app_name = "api"

urlpatterns = [
    path("articles/feed/", SubscribedArticleFeedAPIView.as_view(), name="article-feed"),
    path("publishers/", PublisherListAPIView.as_view(), name="publisher-list"),
]
