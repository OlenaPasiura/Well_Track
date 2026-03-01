from rest_framework import serializers
from .models import UserHealthStats

class HealthStatsSerializer(serializers.ModelSerializer):
    daily_stress = serializers.SerializerMethodField()

    class Meta:
        model = UserHealthStats
        fields = ['id', 'user', 'date', 'sleep_hours', 'mood_score', 'daily_stress']
        read_only_fields = ['user']
    def get_daily_stress(self, obj):
        return obj.calculate_daily_stress()