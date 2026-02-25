from django.contrib import admin
from .models import Profile, StressTracker, Nutrition, SleepRecord, DieticianClient
admin.site.register(Profile)

@admin.register(StressTracker)
class StressTrackerAdmin(admin.ModelAdmin):
    list_display = ('user', 'level', 'created_at', 'notes')
    list_filter = ('level', 'created_at', 'user')

@admin.register(Nutrition)
class NutritionAdmin(admin.ModelAdmin):
    list_display = ('user', 'food_name', 'meal_type', 'calories','fibre','protein', 'fat', 'carbs', 'created_at')
    list_filter = ('meal_type', 'created_at', 'user')
    search_fields = ('food_name',)

@admin.register(SleepRecord)
class SleepRecordAdmin(admin.ModelAdmin):
    list_display = ('user', 'start_time', 'end_time', 'duration', 'created_at')

@admin.register(DieticianClient)
class DieticianClientAdmin(admin.ModelAdmin):
    list_display = ('dietician', 'client', 'assigned_at')
    list_filter = ('dietician', 'assigned_at')
