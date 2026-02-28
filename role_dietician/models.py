from django.db import models
from django.conf import settings

from .validators import validate_nutrition_limit, validate_feedback_text


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

    class Meta:
        verbose_name = "Ціль харчування"
        verbose_name_plural = "Цілі харчування"

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

    class Meta:
        verbose_name = "Фідбек дієтолога"
        verbose_name_plural = "Фідбеки дієтологів"
        ordering = ['-created_at']

    def __str__ (self):
        return f"Порада для {self.client.email} від {self.created_at.date()}"


