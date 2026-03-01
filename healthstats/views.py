from rest_framework import viewsets, permissions
from .models import UserHealthStats
from .serializers import HealthStatsSerializer

class HealthStatsViewSet(viewsets.ModelViewSet):
    serializer_class = HealthStatsSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return UserHealthStats.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)