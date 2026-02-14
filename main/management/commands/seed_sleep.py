from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
import random
from main.models import SleepRecord

class Command(BaseCommand):
    help = "Generate random sleep records"

    def handle (self, *args, **kwargs):
        user = User.objects.first()

        for i in range (35):
            day = timezone.now() - timedelta(days=i)
            hours = random.uniform(5, 9)

            start_time = day - timedelta(hours=hours)
            end_time = day

            SleepRecord.objects.create(
                user=user,
                start_time = start_time,
                end_time = end_time,
                created_at = day.date()
            )

        self.stdout.write(self.style.SUCCESS("Sleep records created!"))