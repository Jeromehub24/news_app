"""URL routes for the public site, publishing tools, and moderation pages."""

from django.urls import path

from .views import (
    ApproveArticleView,
    ArticleCreateView,
    ArticleDeleteView,
    ArticleDetailView,
    ArticleListView,
    ArticleUpdateView,
    HomePageView,
    NewsletterCreateView,
    NewsletterDeleteView,
    NewsletterListView,
    NewsletterUpdateView,
    PublisherCreateView,
    PublisherMembershipToggleView,
    PublisherListView,
    ReviewQueueView,
)


app_name = "core"

urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path("articles/", ArticleListView.as_view(), name="article-list"),
    path("articles/create/", ArticleCreateView.as_view(), name="article-create"),
    path("articles/<int:pk>/", ArticleDetailView.as_view(), name="article-detail"),
    path(
        "articles/<int:pk>/edit/",
        ArticleUpdateView.as_view(),
        name="article-update",
    ),
    path(
        "articles/<int:pk>/delete/",
        ArticleDeleteView.as_view(),
        name="article-delete",
    ),
    path(
        "articles/<int:pk>/approve/",
        ApproveArticleView.as_view(),
        name="article-approve",
    ),
    path("review/", ReviewQueueView.as_view(), name="review-queue"),
    path("newsletters/", NewsletterListView.as_view(), name="newsletter-list"),
    path(
        "newsletters/create/",
        NewsletterCreateView.as_view(),
        name="newsletter-create",
    ),
    path(
        "newsletters/<int:pk>/edit/",
        NewsletterUpdateView.as_view(),
        name="newsletter-update",
    ),
    path(
        "newsletters/<int:pk>/delete/",
        NewsletterDeleteView.as_view(),
        name="newsletter-delete",
    ),
    path("publishers/", PublisherListView.as_view(), name="publisher-list"),
    path(
        "publishers/create/",
        PublisherCreateView.as_view(),
        name="publisher-create",
    ),
    path(
        "publishers/<int:pk>/membership/",
        PublisherMembershipToggleView.as_view(),
        name="publisher-membership",
    ),
]
