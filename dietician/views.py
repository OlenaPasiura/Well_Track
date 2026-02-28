from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from nutrition.models import Nutrition
from sleep_tracker.models import SleepRecord
from stress_tracker.models import StressRecord

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


def view_patient_stats(request, patient_id):
    from django.http import JsonResponse
    from stress_tracker.models import StressRecord
    stats = StressRecord.objects.filter(user_id=patient_id).order_by('created_at')

    # дані для фронтенду
    data = {
        'labels': [record.created_at.strftime("%d.%m") for record in stats],
        'stress_levels': [record.level for record in stats],
        'critical_count': sum(1 for r in stats if r.check_danger_threshold()) # твій метод
    }

    return JsonResponse(data)
#дані про стрес левел конкретного користувача
