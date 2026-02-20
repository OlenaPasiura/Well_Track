from django.db import models
from django.conf import settings

class SleepRecord(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    created_at = models.DateField()

    def __str__(self):
        return f"{self.user} {self.created_at}: {self.duration:.2f} годин."

    @property
    def duration(self):
        """sleep duration."""
        delta = self.end_time - self.start_time
        return max(delta.total_seconds() / 3600, 0)



