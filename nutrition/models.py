from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Nutrition(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    meals_count = models.PositiveIntegerField()

    proteins = models.FloatField
    fats = models.FloatField
    carbs = models.FloatField
    fiber = models.FloatField

    calories = models.FloatField(blank=True, null=True)

    def calculate_calories(self):
        return (self.proteins * 4 + self.carbs * 4 +
                self.fats * 9 + self.fiber * 2)

    def save(self, *args, **kwards):
        self.calories = self.calculate_calories()
        super().save(*args, **kwards)

    def __str__(self):
        return f"{self.user} - {self.date}"
