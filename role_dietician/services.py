from django.contrib.auth import get_user_model
from django.utils import timezone
from .models import NutritionGoal, DieticianFeedback
from .validators import validate_nutrition_limit, validate_feedback_text
from stress_tracker.models import StressRecord
from healthstats.models import UserHealthStats
from user.role import Role

User = get_user_model()

class DieticianService:

    @staticmethod
    def filter_at_risk_users(threshold_percent=80):
        """
        Finds customers in the risk zone.
        Uses the score from StressRecord and % from HealthStats.
        """

        at_risk_list = []
        today = timezone.now().date()

        clients = User.objects.filter(profile_type=Role.USER)

        for client in clients:
            avg_score = StressRecord.calculate_average_stress(client)
            stats = UserHealthStats.objects.filter(user=client, date=today).first()
            calculated_stress_percent = stats.calculate_daily_stress() if stats else 0

            if avg_score >= 4 or calculated_stress_percent >= threshold_percent:
                at_risk_list.append({
                    'user': client,
                    'avg_score': avg_score,
                    'stress_percent': calculated_stress_percent,
                    'has_stats_today': stats is not None
                })

        return at_risk_list


    @staticmethod
    def set_nutrition_goals(user, proteins, fats, carbs, kcal):
        """sets limits of macros for specific user"""

        for val in [proteins, fats, carbs, kcal]:
            validate_nutrition_limit(val)

        goal, created = NutritionGoal.objects.update_or_create(
            user=user,
            defaults={
                'protein_limit': proteins,
                'fat_limit': fats,
                'carbohydrate_limit': carbs,
                'kcal_limit': kcal
            }
        )
        return goal

    @staticmethod
    def send_feedback(dietician, client, message_text):
        """saves nutritionists advise in database """
        validate_feedback_text(message_text)

        return DieticianFeedback.objects.create(
            dietician=dietician,
            client=client,
            message=message_text
        )

    @staticmethod
    def notify_all_at_risk_clients(dietician, custom_message=None):
        """
        Знаходить усіх клієнтів зі стресом > 80% (або середнім балом >= 4)
        і автоматично створює для них фідбек.
        """
        at_risk_data = DieticianService.filter_at_risk_users(threshold_percent=80)

        feedbacks_created = []

        for entry in at_risk_data:
            client = entry['user']
            stress_val = entry['stress_percent']

            text = custom_message or f"Система зафіксувала високий рівень стресу ({stress_val}%). Зверніть увагу на свій стан!"

            fb = DieticianService.send_feedback(
                dietician=dietician,
                client=client,
                message_text=text
            )
            feedbacks_created.append(fb)

        return feedbacks_created