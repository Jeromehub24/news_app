from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from .constants import Roles
from .models import CustomUser
from core.models import Publisher


class CustomUserCreationForm(UserCreationForm):
    role = forms.ChoiceField(choices=Roles.CHOICES)

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ("username", "email", "role")


class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = CustomUser
        fields = (
            "username",
            "email",
            "role",
            "subscribed_publishers",
            "subscribed_journalists",
        )


class ReaderSubscriptionForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ("subscribed_publishers", "subscribed_journalists")
        widgets = {
            "subscribed_publishers": forms.SelectMultiple(attrs={"size": 8}),
            "subscribed_journalists": forms.SelectMultiple(attrs={"size": 8}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["subscribed_publishers"].queryset = Publisher.objects.order_by(
            "name"
        )
        self.fields["subscribed_journalists"].queryset = (
            CustomUser.objects.filter(role=Roles.JOURNALIST).order_by("username")
        )
        self.fields["subscribed_publishers"].help_text = (
            "Choose the publishers you want included in your reader feed."
        )
        self.fields["subscribed_journalists"].help_text = (
            "Choose the journalists you want included in your reader feed."
        )
