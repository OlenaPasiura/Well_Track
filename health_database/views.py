from django.shortcuts import render, redirect
from django.contrib.auth import login
from .models import Profile
from .presentation_layer_userregistration import UserRegistrationForm

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            Profile.objects.create(
                user=user,
                gender=form.cleaned_data['gender'],
                profile_type=form.cleaned_data['profile_type'],
                birth_date=form.cleaned_data.get('birth_date')
            )
            login(request, user)
            return redirect('home')
    else:
        form = UserRegistrationForm()
    return render(request, 'sleep_tracker/register.html', {'form': form})
