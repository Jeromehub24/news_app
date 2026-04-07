from django.urls import path

from .views import (
    ApproveArticleView,
    ArticleCreateView,
    ArticleDetailView,
    ArticleListView,
    ArticleUpdateView,
    HomePageView,
    NewsletterCreateView,
    NewsletterListView,
    PublisherListView,
    ReviewQueueView,
)


app_name = "core"

urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path("articles/", ArticleListView.as_view(), name="article-list"),
    path("articles/create/", ArticleCreateView.as_view(), name="article-create"),
    path("articles/<int:pk>/", ArticleDetailView.as_view(), name="article-detail"),
    path("articles/<int:pk>/edit/", ArticleUpdateView.as_view(), name="article-update"),
    path("articles/<int:pk>/approve/", ApproveArticleView.as_view(), name="article-approve"),
    path("review/", ReviewQueueView.as_view(), name="review-queue"),
    path("newsletters/", NewsletterListView.as_view(), name="newsletter-list"),
    path("newsletters/create/", NewsletterCreateView.as_view(), name="newsletter-create"),
    path("publishers/", PublisherListView.as_view(), name="publisher-list"),
]
