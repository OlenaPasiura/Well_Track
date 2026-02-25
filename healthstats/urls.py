from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import HealthStatsViewSet

router = DefaultRouter()
router.register(r'health-stats', HealthStatsViewSet, basename='health-stats')

urlpatterns = router.urls