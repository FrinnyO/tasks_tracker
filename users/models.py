from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name="Почта")
    phone_number = models.CharField(
        max_length=15, blank=True, null=True, verbose_name="Телефон"
    )
    country = models.CharField(
        max_length=50, blank=True, null=True, verbose_name="Страна"
    )
    avatar = models.ImageField(
        upload_to="avatars/",
        default="users/default_avatar.jpg",
        blank=True,
        null=True,
        verbose_name="Фото",
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email
