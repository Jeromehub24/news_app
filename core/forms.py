from django import forms

from accounts.constants import Roles

from .models import Article, Newsletter, Publisher


class PublisherScopedFormMixin:
    def __init__(self, *args, user=None, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)
        publisher_field = self.fields.get("publisher")
        if not publisher_field:
            return

        queryset = self.get_publisher_queryset()
        if self.instance.pk and self.instance.publisher_id:
            queryset = queryset | Publisher.objects.filter(
                pk=self.instance.publisher_id
            )

        # Journalists can only publish under organizations they have joined.
        publisher_field.queryset = queryset.distinct().order_by("name")
        if (
            self.user
            and self.user.is_authenticated
            and self.user.role == Roles.JOURNALIST
        ):
            publisher_field.help_text = (
                "Choose a publisher you have joined, or leave this blank for an "
                "independent draft."
            )

    def get_publisher_queryset(self):
        if not self.user or not self.user.is_authenticated:
            return Publisher.objects.none()
        if self.user.role == Roles.JOURNALIST:
            return self.user.journalist_publications.all()
        return Publisher.objects.all()


class ArticleForm(PublisherScopedFormMixin, forms.ModelForm):
    class Meta:
        model = Article
        fields = ("publisher", "title", "summary", "content")


class NewsletterForm(PublisherScopedFormMixin, forms.ModelForm):
    class Meta:
        model = Newsletter
        fields = ("publisher", "subject", "body")


class PublisherForm(forms.ModelForm):
    class Meta:
        model = Publisher
        fields = ("name", "description")
