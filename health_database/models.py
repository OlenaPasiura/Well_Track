from datetime import date
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError

class Profile(models.Model):
    '''This class creat dop information about user'''
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birth_date = models.DateField(null=True, blank=True)

    GENDER_CHOICES = [('M', 'Чоловік'), ('F', 'Жінка')]
    ROLE_CHOICES = [('client', 'Клієнт'), ('dietician', 'Дієтолог')]

    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    profile_type = models.CharField(max_length=10, choices=ROLE_CHOICES, default='client')

    @property
    def age_category(self):
        bd = self.birth_date
        if not bd:
            return 'Ви не вказали свої данні в полі про дату народження'
        today = date.today()
        age = today.year - bd.year - ((today.month, today.day) < (bd.month, bd.day))

        if age < 7:
            return 'Дитина дошкільного віку'
        elif 7 <= age <= 12:
            return 'Дитина раннього підліткового віку'
        elif 13 <= age <= 15:
            return 'Підлітковий вік'
        elif 16 <= age <= 19:
            return 'Пізній підлітковий вік'
        elif 20 <= age <= 25:
            return 'Юнацький вік'
        elif 26 <= age <= 45:
            return 'Дорослий вік'
        elif 46 <= age <= 60:
            return "Пізній дорослий вік"
        elif age > 60:
            return 'Похилий вік'
    def __str__(self):
        return f'Профіль {self.user.username} ({self.age_category})'

class StressTracker(models.Model):
    STRESS_LEVELS = [(i, str(i)) for i in range(1,6)]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    level = models.IntegerField(choices=STRESS_LEVELS, verbose_name="Рівень стресу")
    notes = models.TextField(blank=True, null=True, verbose_name="Що сталося? (нотатки)")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата запису")

    def __str__(self):
        return f"{self.user.username} - Рівень: {self.level} ({self.created_at.strftime('%d.%m %H:%M')})"

    class Meta:
        verbose_name = "Запис стресу"
        verbose_name_plural = "Записи стресу"

class Nutrition(models.Model):
    MEAL_CHOICES = [
        ('breakfast', 'Сніданок'),
        ('lunch', 'Обід'),
        ('dinner', 'Вечеря'),
        ('snack', 'Перекус'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    food_name = models.CharField(max_length=255, verbose_name="Назва страви/продукту")
    meal_type = models.CharField(max_length=20, choices=MEAL_CHOICES, verbose_name="Прийом їжі")

    calories = models.PositiveIntegerField(
        validators=[MinValueValidator(0)],
        verbose_name="Калорії (ккал)"
    )
    protein = models.FloatField(
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name="Білки (г)"
    )
    fat = models.FloatField(
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name="Жири (г)"
    )
    carbs = models.FloatField(
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name="Вуглеводи (г)"
    )
    fibre = models.FloatField(
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name="Клітковина (г)"
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата та час запису")

    def __str__(self):
        return f"{self.user.username} - {self.food_name} ({self.calories} ккал)"

    class Meta:
        verbose_name = "Запис харчування"
        verbose_name_plural = "Записи харчування"

class SleepRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_time = models.DateTimeField(verbose_name="Ліг спати")
    end_time = models.DateTimeField(verbose_name="Прокинувся")
    created_at = models.DateTimeField(auto_now_add=True)
    def clean(self):
        if self.start_time and self.end_time:
            if self.end_time <= self.start_time:
                raise ValidationError("Час прокидання має бути пізніше часу, коли ви лягли спати!")

    @property
    def duration(self):
        if self.start_time and self.end_time:
            diff = self.end_time - self.start_time
            hours = diff.total_seconds() / 3600
            return f"{round(hours, 1)} год"
        return "Не вказано"

    def __str__(self):
        return f"{self.user.username} - Сон {self.created_at.strftime('%d.%m')}"

    class Meta:
        verbose_name = "Запис сну"
        verbose_name_plural = "Записи сну"


class DieticianClient(models.Model):
    dietician = models.ForeignKey(User, on_delete=models.CASCADE, related_name='clients', limit_choices_to={'profile__profile_type': 'dietician'}, verbose_name="Дієтолог")
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='dieticians', limit_choices_to={'profile__profile_type': 'client'}, verbose_name="Клієнт")
    assigned_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата закріплення")

    class Meta:
        verbose_name = "Зв'язок Дієтолог-Клієнт"
        verbose_name_plural = "Зв'язки Дієтолог-Клієнт"
        unique_together = ('dietician', 'client')

    def __str__(self):
        return f"Дієтолог {self.dietician.username} -> Клієнт {self.client.username}"
