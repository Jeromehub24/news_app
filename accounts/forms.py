from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from .constants import Roles
from .models import CustomUser


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
