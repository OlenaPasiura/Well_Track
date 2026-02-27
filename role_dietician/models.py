from django.db import models
from django.conf import settings

from .validators import validate_nutrition_limit, validate_feedback_text
from django.core.exceptions import PermissionDenied

from django.db.models import Sum
from datetime import timedelta
from django.utils import timezone
from nutrition.models import Nutrition


class NutritionGoal(models.Model):
    """model to implement set_nutrition_goals"""
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name = 'nutrition_goal'
    )

    protein_limit = models.FloatField(
        verbose_name="Ліміт білків (г)",
        validators = [validate_nutrition_limit]
    )
    fat_limit = models.FloatField(
        verbose_name="Ліміт жирів (г)",
        validators = [validate_nutrition_limit]
    )
    carbohydrate_limit = models.FloatField(
        verbose_name="Ліміт вуглеводів (г)",
        validators = [validate_nutrition_limit]
    )
    kcal_limit = models.FloatField(
        verbose_name="Ліміт калорій (ккал)",
        validators=[validate_nutrition_limit]
    )

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Цілі харчування для {self.user.email}"

class DieticianFeedback(models.Model):
    """model to implement send_feedback"""
    dietician = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='given_feedbacks',
        verbose_name="Дієтолог"
    )
    client = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete = models.CASCADE,
        related_name='received_feedbacks'
    )

    message = models.TextField(
        verbose_name ="Текст поради",
        validators=[validate_feedback_text]
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__ (self):
        return f"Порада для {self.client.email} від {self.created_at.date()}"


class DieticianClient(models.Model):
    dietician = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="clients"
    )
    client = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="assigned_dietician"
    )

    class Meta:
        unique_together = ("dietician", "client")

    def __str__(self):
        return f"{self.dietician.email} → {self.client.email}"


def verify_access(dietician, client):
    """
    Перевіряє, чи дієтолог має доступ до клієнта
    """

    if dietician.role != "dietician":
        raise PermissionDenied("Користувач не є дієтологом")

    if client.role != "client":
        raise PermissionDenied("Цей користувач не є клієнтом")

    if not dietician.patients.filter(id=client.id).exists():
        raise PermissionDenied("У вас немає доступу до цього клієнта")

    return True


def assign_patient(dietician, client):
    """
    Призначає клієнта дієтологу
    """

    if dietician.role != "dietician":
        raise PermissionDenied("Лише дієтолог може призначати клієнтів")

    if client.role != "client":
        raise ValueError("Можна призначати тільки клієнтів")

    dietician.patients.add(client)

    return f"Клієнт {client.email} успішно призначений"



def analyze_nutrition_logs(dietician, client, days=7):
    """
    Аналізує харчові логи клієнта за останні N днів
    """

    verify_access(dietician, client)

    start_date = timezone.now().date() - timedelta(days=days)

    logs = Nutrition.objects.filter(
        user=client,
        date__gte=start_date
    )

    totals = logs.aggregate(
        total_protein=Sum("protein"),
        total_fat=Sum("fat"),
        total_carbohydrate=Sum("carbohydrate"),
        total_kcal=Sum("kcal"),
    )

    goal = client.nutrition_goal

    analysis = {
        "protein_diff": totals["total_protein"] - goal.protein_limit,
        "fat_diff": totals["total_fat"] - goal.fat_limit,
        "carb_diff": totals["total_carbohydrate"] - goal.carbohydrate_limit,
        "kcal_diff": totals["total_kcal"] - goal.kcal_limit,
    }

    return {
        "period_days": days,
        "totals": totals,
        "goal": {
            "protein": goal.protein_limit,
            "fat": goal.fat_limit,
            "carbohydrate": goal.carbohydrate_limit,
            "kcal": goal.kcal_limit,
        },
        "analysis": analysis,
    }
