from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.db.models import Q
from django.utils import timezone

from accounts.constants import Roles


User = get_user_model()


def collect_article_subscribers(article):
    query = Q(subscribed_journalists=article.author)
    if article.publisher_id:
        query |= Q(subscribed_publishers=article.publisher)
    return User.objects.filter(query, role=Roles.READER).distinct()


def send_article_approval_email(article):
    recipients = [user.email for user in collect_article_subscribers(article) if user.email]
    if not recipients:
        return 0

    return send_mail(
        subject=f"New article approved: {article.title}",
        message=article.summary or article.content[:300],
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=recipients,
        fail_silently=True,
    )


def post_article_to_x(article):
    return False


def approve_article(article, editor=None):
    article.approved = True
    article.approved_at = timezone.now()
    article.published_at = article.published_at or timezone.now()
    article.save()

    send_article_approval_email(article)
    post_article_to_x(article)
    return article
