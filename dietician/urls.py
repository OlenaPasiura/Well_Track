from django.urls import path
from . import views

urlpatterns = [
    path('clients/', views.get_my_clients, name='my_clients'),
    path('patient/<int:patient_id>/stats/', views.view_patient_stats, name='patient_stats'),
    path('patient/<int:patient_id>/summary/', views.get_daily_summary, name='daily_summary'),
]
