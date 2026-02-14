from django.shortcuts import render, redirect
from .forms import SleepInputForm
# Create your views here.

def dashboard(request):
    if request.method == 'POST':
        form = SleepInputForm(request.POST)
        if form.is_valid():
            # Поки що просто друкуємо в термінал, щоб перевірити, чи працює
            hours = form.cleaned_data['hours']
            print(f"--- ДАНІ ОТРИМАНО: {hours} годин ---")
            return redirect('dashboard')
    else:
        # Якщо це просто відкриття сторінки (GET)
        form = SleepInputForm()
    # Call functions from models.py
    # This is fake data to check the layout
    context = {
        'form': form,
        'last_night': '5h 12m',
        'week_avg': '5h 31m',
        'month_avg': '6h 46m',
        'chart_data': [7, 8, 5, 9, 8, 6, 6, 5, 6], # Дані для графіка
        'labels': ['15/1', '16/1', '17/1', '18/1', '19/1', '20/1', '21/1', '22/1', '23/1']
    }
    return render(request, 'sleep_tracker/index.html', context)
