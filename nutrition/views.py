from datetime import datetime

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .services import NutritionService
from .validators import NutritionValidationError

@login_required
def create_nutrition_view(request):
    if request.method == "POST":
        try:
            data = {
            'date': datetime.strptime(request.POST.get("gate"), "%d-%m-Y").date(),

            "meals_count": int(request.POST.get("meals_count")),

            "protein": float(request.POST.get("protein")),
            "fat": float(request.POST.get("fat")),
            "carbs": float(request.POST.get("carbs")),
                "fiber": float(request.POST.get("fiber")),
            }

            NutritionService.create_entry(user=request.user, data=data)

            messages.success(request, "Nutrition enry created!")
            return redirect("nutrition_list")

        except ValueError:
            messages.error(request, "Invalid input format.")

        except NutritionValidationError as e:
            messages.error(request, str(e))

    return render(request, "nutrition/create.html")
