from django.db import models

class Role(models.TextChoices):
    USER = "USER", "Користувач"
    DIETITIAN = "DIETITIAN", "Дієтолог"