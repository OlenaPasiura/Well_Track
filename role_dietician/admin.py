from django.contrib import admin
from .models import NutritionGoal, DieticianFeedback
from .services import DieticianService
from user.role import Role
from django.contrib import messages

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


@admin.action(description="Надіслати попередження про стрес (>80%) обраним")
def notify_stress_action(modeladmin, request, queryset):
    """
    Action для адмінки: дозволяє вибрати юзерів і автоматично
    перевірити їхній стрес через наш сервіс.
    """
    if request.user.profile_type != Role.DIETITIAN:
        modeladmin.message_user(request, "Тільки дієтологи можуть це робити", messages.ERROR)
        return

    # Викликаємо метод сервісу, який ми обговорювали раніше
    sent_count = len(DieticianService.notify_all_at_risk_clients(dietician=request.user))

    modeladmin.message_user(
        request,
        f"Успішно перевірено базу. Створено {sent_count} повідомлень для клієнтів у зоні ризику.",
        messages.SUCCESS
    )