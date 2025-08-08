from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, logout
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.urls import reverse_lazy
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

class CustomLoginView(LoginView):
    def get_success_url(self):
        user = self.request.user
        if user.role == 'teacher':
            return reverse_lazy('user:teacher_dashboard')
        elif user.role == 'parent':
            return reverse_lazy('user:parent_dashboard')
        return reverse_lazy('user:home')
    
@login_required
def teacher_dashboard(request):
    if request.user.role != 'teacher':
        return HttpResponseForbidden("You are not allowed to access this page.")
    return render(request, 'user/teacher_dashboard.html')

@login_required
def parent_dashboard(request):
    if request.user.role != 'parent':
        return HttpResponseForbidden("You are not allowed to access this page.")
    return render(request, 'user/parent_dashboard.html')

def logout_view(request):
    logout(request)
    messages.success(request, "Logout successful.")
    return redirect('user:home')