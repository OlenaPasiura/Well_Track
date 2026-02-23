from rest_framework import serializers
from .models import HealthStats

class HealthStatsSerializer(serializers.ModelSerializer):
    daily_stress = serializers.SerializerMethodField()

    class Meta:
        model = HealthStats
        fields = ["id", "date", "sleep_hours", "mood_score", "daily_stress"]

    def get_daily_stress(self, obj):
        return obj.calculate_daily_stress()