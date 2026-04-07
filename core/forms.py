from django import forms

from accounts.models import CustomUser

from .models import Article, Newsletter


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ("publisher", "title", "summary", "content")


class NewsletterForm(forms.ModelForm):
    class Meta:
        model = Newsletter
        fields = ("publisher", "subject", "body")


class ReaderSubscriptionForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ("subscribed_publishers", "subscribed_journalists")
