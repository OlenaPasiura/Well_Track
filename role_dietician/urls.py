from django.urls import path
from . import views

urlpatterns = [
    path('set-goals/<int:client_id>/', views.set_goals_view, name='set_nutrition_goals'),
    path('send-feedback/<int:client_id>/', views.send_feedback_view, name='send_feedback'),
    path('at-risk/', views.at_risk_list_view, name='at_risk_list'),
    path('at-risk/notify-all/', views.notify_all_at_risk_view, name='notify_all_at_risk'),
]