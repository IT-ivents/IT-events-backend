from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Кастомная модель пользователя"""

    ADMIN = "admin"
    USER = "user"
    MANAGER = "manager"
    role_choices = (
        (ADMIN, ADMIN),
        (USER, USER),
        (MANAGER, MANAGER)
    )
    email = models.EmailField("email address", unique=True)
    role = models.CharField(
        max_length=settings.USER_ROLE_NAME_LENGTH,
        choices=role_choices, default=USER
    )
    profile_photo = models.ImageField("Аватар", upload_to="users/avatars/",
                                      help_text="Аватар пользователя",
                                      blank=True)

    @property
    def is_admin(self):
        return self.role == self.ADMIN

    @property
    def is_manager(self):
        return self.role == self.MANAGER

    class Meta:
        ordering = ["-id"]
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class Organisation(models.Model):
    manager = models.OneToOneField(User,
                                   on_delete=models.CASCADE,
                                   related_name="organization",
                                   verbose_name="Менеджер организации")
    name = models.CharField(max_length=200, db_index=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Организация"
        verbose_name_plural = "Организации"
