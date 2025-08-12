from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, logout
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse_lazy
from .forms import SignupForm
from .decorators import role_required


def home_view(request):
    """
    Render the homepage view.
    """
    return render(request, 'user/home.html')


User = get_user_model()


def signup_view(request):
    """
    Handle user signup.
    """
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,
                             "Account created successfully! Please log in.")
            return redirect('user:login')
    else:
        form = SignupForm()
    return render(request, 'user/signup.html', {'form': form})


class CustomLoginView(LoginView):
    """
    Custom login view that redirects users based on their role after login.
    """
    def get_success_url(self):
        """
        Determine the redirect URL after a successful login.
        """
        user = self.request.user
        if user.role == 'teacher':
            return reverse_lazy('user:teacher_dashboard')
        elif user.role == 'parent':
            return reverse_lazy('user:parent_dashboard')
        return reverse_lazy('user:home')


@login_required
@role_required('teacher')
def teacher_dashboard(request):
    """
    Display the teacher's dashboard.
    """
    return render(request, 'user/teacher_dashboard.html')


@login_required
@role_required('parent')
def parent_dashboard(request):
    """
    Display the parent's dashboard.
    """
    return render(request, 'user/parent_dashboard.html')


def logout_view(request):
    """
    Log the user out and redirect to the home page.
    """
    logout(request)
    messages.success(request, "Logout successful.")
    return redirect('user:home')
