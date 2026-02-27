from django.contrib import admin
from .models import NutritionGoal, DieticianFeedback

@admin.register(NutritionGoal)
class NutritionGoalAdmin(admin.ModelAdmin):
    """Configuring the display of macros norms """
    list_display = ('user', 'protein_limit', 'fat_limit', 'carbohydrate_limit', 'kcal_limit')
    search_fields = ('user__username', 'user__email')
    list_filter = ('kcal_limit',)

@admin.register(DieticianFeedback)
class DieticianFeedbackAdmin(admin.ModelAdmin):
    """setting up diaplay of advice"""
    list_display = ('dietician', 'client', 'message', 'created_at') # Додав дату, якщо вона є в моделі
    search_fields = ('dietician__email', 'client__username', 'message')
    list_filter = ('dietician',)