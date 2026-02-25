from django.contrib import admin
from .models import SleepRecord

@admin.register(SleepRecord)
class SleepRecordAdmin(admin.ModelAdmin):
    list_display = ('user', 'start_time', 'end_time')

# Register your models here.
