from django.db import models
from django.contrib.auth.models import AbstractUser
from .role import Role
from .user_manager import UserManager


class User(AbstractUser):
    email = models.EmailField(unique=True)
    gender = models.CharField(max_length=20, blank=True)
    age = models.IntegerField(null=True, blank=True)

    profile_type = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.USER
    )
    username = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email