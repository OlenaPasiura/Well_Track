from rest_framework import serializers
from .models import NutritionGoal, DieticianFeedback
from .validators import validate_nutrition_limit, validate_feedback_text

class NutritionGoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = NutritionGoal
        fields = ['id', 'user', 'protein_limit', 'fat_limit', 'carbohydrate_limit', 'kcal_limit']
        read_only_fields = ['user']

class DieticianFeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = DieticianFeedback
        fields = ['id', 'client', 'message', 'created_at']
        read_only_fields = ['dietician']