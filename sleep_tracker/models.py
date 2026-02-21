from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class SleepRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} {self.created_at}: {self.duration:.2f} годин."

    @property
    def duration (self):
        """sleep duration."""
        delta = self.end_time - self.start_time
        return max (delta.total_seconds() / 3600, 0)

    def clean(self):
        if self.end_time <= self.start_time:
            raise ValidationError("End time must be after start time.")
