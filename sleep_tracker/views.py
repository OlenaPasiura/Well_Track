from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta
from .forms import SleepInputForm
from .models import SleepRecord

@login_required
def dashboard(request):

    if request.method == "POST":
        form = SleepInputForm(request.POST)
        if form.is_valid():
            SleepRecord.objects.create(
                user=request.user,
                start_time = form.cleaned_data["start_time"],
                end_time = form.cleaned_data["end_time"],
                created_at = timezone.now().date()
            )
            return redirect("dashboard")

    else:
        form = SleepInputForm()

    records = SleepRecord.objects.filter(
        user=request.user
    ).order_by("start_time")

    last_record = records.last()
    last_night = (
        f"{last_record.duration:.2f}h" if last_record else "No data"
    )

    week_ago = timezone.now() - timedelta(days=7)
    week_records = records.filter(start_time__gte = week_ago)

    week_avg = (sum(r.duration for r in week_records) / week_records.count()
                if week_records.exists() else None)

    week_avg = f"{week_avg:.2f}h" if week_avg else "No data"


    month_ago = timezone.now() - timedelta(days=30)
    month_records = records.filter(start_time__gte=month_ago)

    month_avg = (sum(r.duration for r in month_records) / month_records.count()
        if month_records.exists() else None)

    month_avg = f"{month_avg:.2f}h" if month_avg else "No data"

    chart_records = records.order_by("-start_time")[:9][::-1]

    chart_data = [round(r.duration, 2) for r in chart_records]
    labels = [
        r.start_time.strftime("%d/%m")
        for r in chart_records
    ]

    context = {
        "form": form,
        "last_night": last_night,
        "week_avg": week_avg,
        "month_avg": month_avg,
        "chart_data": chart_data,
        "labels": labels,
    }

    

    return render(request, "sleep_tracker/index.html", context)
