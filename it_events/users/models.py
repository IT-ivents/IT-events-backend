from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
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
    organization_name = models.CharField(
        max_length=100,
        verbose_name='Организация',
        blank=True
    )
    email = models.EmailField("email address", unique=True)
    username = models.CharField(
        max_length=150,
        unique=False,
    )
    role = models.CharField(
        max_length=settings.USER_ROLE_NAME_LENGTH,
        choices=role_choices, default=USER
    )
    
    USERNAME_FIELD = 'email' 
    REQUIRED_FIELDS = [] 

    @property
    def is_admin(self):
        return self.role == self.ADMIN

    @property
    def is_manager(self):
        return self.role == self.MANAGER

    def clean(self):
        super().clean()
        if not self.organization_name:
            raise ValidationError({'Организация является обязательным полем.'})

    class Meta:
        ordering = ["-id"]
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


# class UserProfile(models.Model):
#     """Личный кабинет организатора."""
#     user = models.OneToOneField(
#         User, on_delete=models.CASCADE, related_name='profile')
#     email = models.EmailField("Email address", unique=True)
#     profile_photo = models.ImageField("Аватар", upload_to="users/avatars/",
#                                       help_text="Аватар пользователя",
#                                       blank=True)
#     organization_name = models.CharField(
#         max_length=100,
#         verbose_name='Организация',
#         blank=True
#     )
#     name = models.CharField(
#         max_length=100,
#         verbose_name='ФИО',
#         blank=True
#     )

#     class Meta:
#         verbose_name = "Личный кабинет"
#         verbose_name_plural = "Личный кабинет"

#     def __str__(self):
#         return self.user.username


class UserEvent(models.Model):
    """События созданные организатором."""
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='user_events')
    event = models.ForeignKey(
        'events.Event', on_delete=models.CASCADE, related_name='event_users')

    def __str__(self):
        return f'{self.user.user.username} - {self.event.title}'

    class Meta:
        ordering = ('-id', )
        verbose_name = 'Список событий организатора'
        verbose_name_plural = 'Список событий организатора'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'event'],
                name='unique_user_event'
            )
        ]


class Organisation(models.Model):
    """Организация пользователя."""
    name = models.CharField(max_length=200, db_index=True)
    manager = models.OneToOneField(User,
                                   on_delete=models.CASCADE,
                                   related_name="organization",
                                   verbose_name="Менеджер организации")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Организация"
        verbose_name_plural = "Организации"
