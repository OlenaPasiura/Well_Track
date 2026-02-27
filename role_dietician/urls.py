from django.urls import path
from . import views

urlpatterns = [
    path('set-goals/<int:client_id>/', views.set_goals_view, name='set_nutrition_goals'),
    path('send-feedback/<int:client_id>/', views.send_feedback_view, name='send_feedback'),
]