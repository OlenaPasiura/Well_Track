from django.contrib import admin
from .models import HealthStats

@admin.register(HealthStats)
class HealthStatsAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'mood_score', 'sleep_hours', 'get_stress')

    list_filter = ('user', 'date')

    search_fields = ('user__username',)


    def get_stress(self, obj):
        return f"{obj.calculate_daily_stress()}%"
    get_stress.short_description = 'Stress Level'