from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from nutrition.models import Nutrition

User = get_user_model()

class UserHealthStats(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name = "health_stats"
    )
    #дата запису
    date = models.DateField(default=timezone.now)

    #кількість годин
    sleep_hours = models.PositiveIntegerField(
        validators=[
            MinValueValidator(0),
            MaxValueValidator(24),
        ],
        help_text="Кількість годин сну не може перевищувати 24"
    )
    mood_score = models.PositiveIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        help_text ="Оцінка настрою від 0 до 5"
    )
    class Meta:
        unique_together = ('user', 'date')
        ordering = ['-date']

    def get_norms_by_gender(self):
        if hasattr (self.user, 'gender') and self.user == 'female':
            return {'protein': 60, 'fat': 55, 'carbs': 220, 'fiber': 25}
        return {'protein': 80, 'fat': 70, 'carbs': 300, 'fiber': 30}

    def calculate_daily_stress(self):
        """
                Головна формула: Сон (32%) + Настрій (30%) + Харчування(38%).
                Разом = 100% максимального стресу.
                """

        mood_penalty = (5 - self.mood_score) * 6 #психологічний стан — це приблизно 1/3 від загального самопочуття людини.
        sleep_penalty = max(0, (8 - self.sleep_hours) * 4) #теж приблизно 1/3 від шкали стресу.

        norms = self.get_norms_by_gender()

        nutrition_penalty = 0
        nutr = Nutrition.objects.filter(user=self.user, date=self.date).first()

        if nutr:
            if nutr.proteins < norms['protein']: nutrition_penalty += 8
            if nutr.fats < norms['fat']: nutrition_penalty += 5
            if nutr.carbs < norms['carbs']: nutrition_penalty += 5
            if nutr.fiber < norms['fiber']: nutrition_penalty += 5

            if nutr.meals_count < 3:
                nutrition_penalty += 5

            total_kcal = nutr.calculate_calories()
            if total_kcal < (norms['target_kcal'] * 0.8):
                nutrition_penalty += 10

        else:
            nutrition_penalty = 38

        return min(mood_penalty + sleep_penalty + nutrition_penalty, 100)

    def __str__(self):
        return f"Статистика {self.user.username} за {self.date}"


    @classmethod
    def get_average_stress(cls, user, start_date=None, end_date=None):
        records = cls.objects.filter(user=user)

        if start_date:
            records = records.filter(date__gte=start_date)

        if end_date:
            records = records.filter(date__lte=end_date)

        count = records.count()

        if count == 0:
            return 0

        total_stress = sum(record.calculate_daily_stress() for record in records)

        return round (total_stress / count, 1)

    @classmethod
    def get_current_month_stress(cls, user):
        today = timezone.now().date()
        start_month = today.replace(day=1)
        return cls.get_average_stress(user, start_date=start_month, end_date=today)

    def __str__(self):
        return f"{self.user.username} | {self.date}"



