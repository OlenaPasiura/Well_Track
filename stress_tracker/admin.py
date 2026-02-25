from django.contrib import admin
from .models import StressRecord

@admin.register(StressRecord)
class StressRecordAdmin(admin.ModelAdmin):
    list_display = ('user', 'level', 'is_dangerous', 'created_at')
    list_filter = ('level', 'created_at')

    def is_dangerous(self, obj):
        return obj.check_danger_threshold()

    is_dangerous.boolean = True
    is_dangerous.short_description = "Критичний рівень"
