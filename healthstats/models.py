from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

class HealthStats(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name = "health_stats"
    )
    #дата запису
    date = models.DateField(default=timezone.now)

    #кількість годин

    sleep_hours = models.PositiveIntegerField(
        validators=[
            MinValueValidator(0),
            MaxValueValidator(24)
        ]
    )
    mood_score = models.PositiveIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(5)]
    )
    class Meta:
        unique_together = ('user', 'date')
        ordering = ['-date']

    def __str__(self):
        return f"{self.user} - {self.date}"

    def calculate_daily_stress(self):
        sleep_factor = max(0, 8 - self.sleep_hours)
        mood_factor = 5 - self.mood_score

        stress = (sleep_factor * 10) + (mood_factor * 5)

        return min(stress, 100)

    @classmethod
    def get_average_stress(cls, user, start_date=None, end_date=None):
        records = cls.objects.filter(user=user)

        if start_date:
            records = records.filter(date__gte=start_date)

        if end_date:
            records = records.filter(date__lte=end_date)

        count = records.count()

        if count == 0:
            return 0

        total_stress = sum(record.calculate_daily_stress() for record in records)

        return total_stress / count

    @classmethod
    def get_current_month_stress(cls, user):
        today = timezone.now().date()
        start_month = today.replace(day=1)
        return cls.get_average_stress(user, start_date=start_month, end_date=today)



