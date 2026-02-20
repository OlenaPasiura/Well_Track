from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Nutrition(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='nutrition_entries'
    )

    date = models.DateField()

    meals_count = models.PositiveIntegerField()
    proteins = models.FloatField
    fats = models.FloatField
    carbohydrates = models.FloatField
    fiber = models.FloatField

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'date')
        ordering = ['-date']

    def __str__(self):
        return f'{self.user} - {self.date}'

    @property
    def total_calories(self):
        return (self.proteins * 4 + self.carbohydrates * 4 +
                self.fats * 9 + self.fiber * 2)
