from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.contrib.auth import get_user_model
from .services import DieticianService
from user.role import Role


User = get_user_model()

@login_required
def set_goals_view(request, client_id):
    """nutrition goals"""

    if request.user.profile_type != Role.DIETITIAN:
        raise PermissionDenied()

    client = get_object_or_404(User, id=client_id)
    if request.method == "POST":

        p = request.POST.get('proteins')
        f = request.POST.get('fats')
        c = request.POST.get('carbs')
        kcal = request.POST.get('kcal')

        DieticianService.set_nutrition_goals(client, p, f, c, kcal)
        return redirect('at_risk_list')

    return render(request, 'role_dietician/set_goals.html', {'client': client})

@login_required
def send_feedback_view(request, client_id):
    """saves the text of the message from the nutritionist to the client."""

    if request.user.profile_type != Role.DIETITIAN:
        raise PermissionDenied()

    client = get_object_or_404(User, id=client_id)

    if request.method == "POST":
        p = request.POST.get('proteins')
        f = request.POST.get('fats')
        c = request.POST.get('carbs')
        kcal = request.POST.get('kcal')

        DieticianService.set_nutrition_goals(client, p, f, c, kcal)
        return redirect('home')

    return render(request, 'role_dietician/set_goals.html', {'client': client})


@login_required
def at_risk_list_view(request):
    """Відображає список користувачів у зоні ризику (>80%)"""
    if request.user.profile_type != Role.DIETITIAN:
        raise PermissionDenied()
    at_risk_users = DieticianService.filter_at_risk_users(threshold_percent=80)

    return render(request, 'role_dietician/at_risk_list.html', {
        'at_risk_users': at_risk_users
    })


@login_required
def notify_all_at_risk_view(request):
    """Метод для масової розсилки фідбеку всім зі стресом > 80%"""
    if request.user.profile_type != Role.DIETITIAN:
        raise PermissionDenied()

    if request.method == "POST":
        DieticianService.notify_all_at_risk_clients(dietician=request.user)
        return redirect('at_risk_list')

    return redirect('at_risk_list')