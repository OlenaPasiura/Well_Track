from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from nutrition.models import Nutrition
from sleep_tracker.models import SleepRecord
from stress_tracker.models import StressRecord
from django.utils import timezone
from django.db.models import Avg
User = get_user_model()

def view_patient_stats(request, patient_id):
    patient = get_object_or_404(User, id=patient_id)
    stress_data = StressRecord.objects.filter(user=patient).order_by('created_at')
    sleep_data = SleepRecord.objects.filter(user=patient).order_by('created_at')
    nutrition_data = Nutrition.objects.filter(user=patient).order_by('date')

    return JsonResponse({
    "patient": patient.username,
    "stress_history": [
        {"date": s.created_at.strftime('%d.%m'), "level": s.level}
        for s in stress_data
    ],
    "sleep_history": [
        {"date": sl.start_time.strftime('%d.%m'), "duration": sl.duration}
        for sl in sleep_data
    ],
    "nutrition_history": [
        {
            "date": n.date.strftime('%d.%m'),
            "calories": n.calories,
            "proteins": n.proteins,
            "fats": n.fats,
            "carbs": n.carbs,
            "fiber": n.fiber,
            "meals_count": n.meals_count
        }
        for n in nutrition_data
    ]
})

def get_my_clients(request):
    dietician = request.user
    connections = dietician.clients.all()
    clients_list = [
        {"id": c.client.id, "username": c.client.username}
        for c in connections
    ]
    return JsonResponse({"my_clients": clients_list})
 # ми отримуємо список всії людей з їчніми id та показуємо дієтологу всіх,
 #далі він вибирає когось конкретного клікає на нього та отримує весь звіт


def get_daily_summary(request, patient_id):
    patient = get_object_or_404(User, id=patient_id)
    today = timezone.now().date()

    nutrition = Nutrition.objects.filter(user=patient, date=today).first()

    stress_avg = StressRecord.objects.filter(
        user=patient,
        created_at__date=today
    ).aggregate(Avg('level'))['level__avg']

    sleep = SleepRecord.objects.filter(user=patient, start_time__date=today).first()

    return JsonResponse({
        "patient": patient.username,
        "date": today.strftime('%d.%m.%Y'),
        "daily_report": {
            "nutrition": {
                "calories": nutrition.calories if nutrition else 0,
                "proteins": nutrition.proteins if nutrition else 0,
                "fats": nutrition.fats if nutrition else 0,
                "carbs": nutrition.carbs if nutrition else 0,
                "meals": nutrition.meals_count if nutrition else 0
            },
            "stress": {
                "average_level": round(stress_avg, 1) if stress_avg else 0,
                "status": "Check needed" if stress_avg and stress_avg > 7 else "Normal"
            },
            "sleep": {
                "duration_hours": sleep.duration if sleep else 0,
                "quality_score": "Good" if sleep and sleep.duration >= 7 else "Low"
            }
        }
    })
