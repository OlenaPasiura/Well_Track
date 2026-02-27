from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import Avg

class StressRecord(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="sleep_tracker_records")
    level = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name="Рівень стресу"
    )

    notes = models.TextField(blank=True, null=True, verbose_name="Нотатки")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата")

    class Meta:
        verbose_name = "Запис стресу"
        verbose_name_plural = "Записи стресу"

    def __str__(self):
        return f"{self.user.username} - {self.level} ({self.created_at.date()})"

    def check_danger_threshold(self):
        return self.level >= 4

    @staticmethod
    def calculate_average_stress(user):
        average = StressRecord.objects.filter(user=user).aggregate(Avg('level'))['level__avg']
        return round(average, 1) if average else 0

    def get_history(self):
        return StressRecord.objects.filter(user=self.user).order_by('-created_at')

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="stress_records")
