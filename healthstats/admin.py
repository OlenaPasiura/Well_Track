from django.contrib import admin
from .models import HealthStats

@admin.register(HealthStats)
class HealthStatsAdmin(admin.ModelAdmin):
    list_display = ("user", "date", "sleep_hours", "mood_score")
    list_filter = ("date", "user")
    ordering = ("-date",)