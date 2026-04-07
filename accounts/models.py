from django.contrib.auth.models import AbstractUser
from django.db import models

from .constants import Roles


class CustomUser(AbstractUser):
    role = models.CharField(
        max_length=20,
        choices=Roles.CHOICES,
        default=Roles.READER,
        help_text="Controls which pages and permissions the user receives.",
    )
    subscribed_publishers = models.ManyToManyField(
        "core.Publisher",
        blank=True,
        related_name="subscribed_readers",
        help_text="Publishers this reader follows.",
    )
    subscribed_journalists = models.ManyToManyField(
        "self",
        blank=True,
        symmetrical=False,
        related_name="reader_followers",
        limit_choices_to={"role": Roles.JOURNALIST},
        help_text="Journalists this reader follows.",
    )

    def __str__(self):
        return self.get_username()
