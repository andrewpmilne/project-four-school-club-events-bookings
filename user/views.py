from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib import messages

def home_view(request):
    return render(request, 'user/home.html')

User = get_user_model()

def signup_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        name = request.POST.get('name')
        role = request.POST.get('role')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')

        if password != password_confirm:
            messages.error(request, "Passwords do not match.")
            return render(request, 'user/signup.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
            return render(request, 'user/signup.html')

        user = User.objects.create_user(email=email, password=password, role=role, name=name)
        messages.success(request, "Account created successfully! Please log in.")
        return redirect('user:home') 

    return render(request, 'user/signup.html')
