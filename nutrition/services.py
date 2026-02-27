from nutrition.validators import NutritionValidator
from nutrition.models import Nutrition

class NutritionService:

    @staticmethod
    def create_entry(user, data: dict):
        NutritionValidator.validate(data)

        return Nutrition.objects.create(
            user=user,
            protein=data["protein"],
            fat=data["fat"],
            carbs=data["carbs"],
            fiber=data["fiber"],
        )
