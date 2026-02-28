from django.contrib import admin
from django.urls import path, include
from core.views import home
from core import views
from nutrition import views as nutrition_views


urlpatterns = [
    # головна
    path('', home, name='home'),

    # сторінки фронту
    path('login/', views.login_page, name='login_page'),
    path('register/', views.register_page, name='register_page'),
    path('select-type/', views.select_type_page, name='select_type_page'),
    path('dashboard/', views.dashboard_page, name='dashboard_page'),
    path('sleep/', views.sleep_page, name='sleep_page'),
    path('stress/', views.stress_page, name='stress_page'),
    path('nutrition/', views.nutrition_page, name='nutrition_page'),
    path('chat/', views.chat_page, name='chat_page'),
    path('responses/', views.responses_page, name='responses_page'),
    path('dietician/', include('dietician.urls')),
    # адмінка
    path('admin/', admin.site.urls),

    # sleep tracker (окремий додаток)
    path('sleep-tracker/', include('sleep_tracker.urls')),

    # health stats API
    path('api/health/', include('healthstats.urls')),

    # nutrition backend дії
    path("nutrition/create/", nutrition_views.nutrition_create, name="nutrition_create"),
    path("nutrition/delete/<int:pk>/", nutrition_views.nutrition_delete, name="nutrition_delete"),
]
