from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):

    class Roles(models.TextChoices):
        """Абстрактный класс ролей"""
        USER = 'user', 'User'
        MODERATOR = 'moderator', 'Moderator'
        ADMIN = 'admin', 'Admin'

    email = models.EmailField('Почтовый адрес', unique=True, blank=False)
    bio = models.TextField('Информация о пользователе', max_length=150, blank=True)
    role = models.CharField('Роль пользователя', max_length=150, choices=Roles.choices,
                            default=Roles.USER)
    confirmation_code = models.CharField('Код подтверждения', max_length=150, blank=True)

    class Meta:
        verbose_name = 'Пользователь'

    def __str__(self):
        return self.username