from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Кастомная модель пользователя"""

    ADMIN = "admin"
    USER = "user"
    role_choices = (
        (ADMIN, ADMIN),
        (USER, USER),
    )
    role = models.CharField(
        max_length=settings.USER_ROLE_NAME_LENGTH,
        choices=role_choices, default=USER
    )
    profile_photo = models.ImageField("Аватар", upload_to="users/avatars/",
                                      help_text="Аватар пользователя")

    @property
    def is_admin(self):
        return self.role == self.ADMIN

    class Meta:
        ordering = ["-id"]
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
