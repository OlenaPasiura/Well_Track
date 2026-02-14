from datetime import timedelta
from django.utils import timezone
from .models import SleepRecord

def get_avg_sleep (user, days):
    today = timezone.localdate()
    start_date = today - timedelta(days=days-1)

    records = SleepRecord.objects.filter(
     user = user,
        data__range = (start_date, today)
    )

    if not records.exists():
        return 0.0

    total = 0
    for record in records:
        total += record.duration

    return total/records.count()


def get_chart_data(user):
    today = timezone.localdate()
    start_date = today - timedelta(days=30)

    records = SleepRecord.objects.filter(
        user=user,
        data__range = (start_date, today)
    ).order_by ('created at')

    dates = []
    hours = []

    for record in records:
        dates.append(str(record.created_at))
        hours.append(record.duration)

        return dates, hours
