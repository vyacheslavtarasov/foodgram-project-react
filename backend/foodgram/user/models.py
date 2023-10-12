from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models

from foodgram.constans import UserModelsConstants


class CustomUser(AbstractUser):
    """Custom User model"""

    username = models.CharField(
        "Username",
        max_length=UserModelsConstants.NAME_LENGTH.value,
        unique=True,
        validators=[
            RegexValidator(
                regex="^[\\w.@+-]+\\Z",
                message=(
                    "This field must contain digits and characters including"
                    " @/./+/-/_."
                ),
            ),
        ],
    )
    first_name = models.CharField(
        max_length=UserModelsConstants.NAME_LENGTH.value,
        null=False,
        blank=False,
    )
    last_name = models.CharField(
        max_length=UserModelsConstants.NAME_LENGTH.value,
        null=False,
        blank=False,
    )
    email = models.EmailField(
        blank=False,
        max_length=UserModelsConstants.EMAIL_LENGTH.value,
        unique=True,
        verbose_name="email address",
        null=False,
    )
    password = models.CharField(
        "User password",
        max_length=UserModelsConstants.PASSWORD_LENGTH.value,
        null=False,
        blank=False,
    )

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ["-id"]

    REQUIRED_FIELDS = ["username", "first_name", "last_name", "password"]
    USERNAME_FIELD = "email"

    def __str__(self):
        return str(self.username)


class Subscribe(models.Model):
    """Subscribe model"""

    user = models.ForeignKey(
        CustomUser, related_name="users", null=True, on_delete=models.SET_NULL
    )
    user_subscribed_on = models.ForeignKey(
        CustomUser,
        related_name="users_subscribed_on",
        null=True,
        on_delete=models.SET_NULL,
    )

    class Meta:
        verbose_name = "Subscribe"
        verbose_name_plural = "Subscriptions"
        unique_together = (("user", "user_subscribed_on"),)
        ordering = ["id"]

    def __str__(self):
        return f"{self.user} {self.user_subscribed_on}"
