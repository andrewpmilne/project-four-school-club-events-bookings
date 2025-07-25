from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib import messages
from .forms import SignupForm

def home_view(request):
    return render(request, 'user/home.html')

User = get_user_model()

def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully! Please log in.")
            return redirect('user:login')

    else:
        form = SignupForm()
    return render(request, 'user/signup.html', {'form': form})
