from django.shortcuts import render

def home(request):
    return render(request, "index.html")

def login_page(request):
    return render(request, "login.html")

def register_page(request):
    return render(request, "register.html")

def select_type_page(request):
    return render(request, "select-type.html")

def dashboard_page(request):
    return render(request, "dashboard.html")

def sleep_page(request):
    return render(request, "sleep.html")

def stress_page(request):
    return render(request, "stress.html")

def nutrition_page(request):
    return render(request, "nutrition.html")

def chat_page(request):
    return render(request, "chat.html")

def responses_page(request):
    return render(request, "responses.html")
