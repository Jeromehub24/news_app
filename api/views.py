from django.db.models import Q
from rest_framework import generics

from core.models import Article, Publisher

from .permissions import IsAuthenticatedNewsUser
from .serializers import ArticleSerializer, PublisherSerializer


class SubscribedArticleFeedAPIView(generics.ListAPIView):
    serializer_class = ArticleSerializer
    permission_classes = [IsAuthenticatedNewsUser]

    def get_queryset(self):
        user = self.request.user
        publisher_ids = user.subscribed_publishers.values_list("id", flat=True)
        journalist_ids = user.subscribed_journalists.values_list("id", flat=True)

        return (
            Article.objects.filter(approved=True)
            .filter(
                Q(publisher_id__in=publisher_ids) | Q(author_id__in=journalist_ids)
            )
            .select_related("publisher", "author")
            .distinct()
        )


class PublisherListAPIView(generics.ListAPIView):
    queryset = Publisher.objects.all()
    serializer_class = PublisherSerializer
    permission_classes = [IsAuthenticatedNewsUser]
