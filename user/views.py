from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, logout
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse_lazy
from .forms import SignupForm
from .decorators import role_required
import re


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

        # Extract raw POST data
        email = request.POST.get('email', '').strip()
        first_name = request.POST.get('first_name', '').strip()
        surname = request.POST.get('surname', '').strip()
        role = request.POST.get('role', '').strip()
        password = request.POST.get('password', '')
        password_confirm = request.POST.get('password_confirm', '')

        # Check required fields
        required_fields = {
            'email': email,
            'first_name': first_name,
            'surname': surname,
            'role': role,
            'password': password,
            'password_confirm': password_confirm,
        }
        for field, value in required_fields.items():
            if not value:
                messages.error(
                    request,
                    f"{field.replace('_', ' ').capitalize()} is required."
                )
                return render(request, 'user/signup.html', {'form': form})

        # Teacher email validation
        if role == 'teacher' and not email.endswith('.sch.uk'):
            messages.error(
                request,
                "Teachers must sign up with an email address "
                "ending in '.sch.uk'."
            )
            return render(request, 'user/signup.html', {'form': form})

        # Password validations
        if password != password_confirm:
            messages.error(request, "Passwords do not match.")
            return render(request, 'user/signup.html', {'form': form})

        if len(password) < 8:
            messages.error(
                request,
                "Password must be at least 8 characters long."
            )
            return render(request, 'user/signup.html', {'form': form})

        if not re.search(r'[A-Z]', password):
            messages.error(
                request,
                "Password must contain at least one uppercase letter."
            )
            return render(request, 'user/signup.html', {'form': form})

        if not re.search(r'\d', password):
            messages.error(
                request,
                "Password must contain at least one number."
            )
            return render(request, 'user/signup.html', {'form': form})

        if not re.search(r'[!@#$%^&*(),.?\":{}|<>]', password):
            messages.error(
                request,
                "Password must contain at least one special character."
            )
            return render(request, 'user/signup.html', {'form': form})

        # Check for duplicate email
        if User.objects.filter(email=email).exists():
            messages.error(
                request,
                "An account with this email already exists."
            )
            return render(request, 'user/signup.html', {'form': form})

        # Only call form.is_valid() after view-level checks pass
        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Account created successfully! Please log in."
            )
            return redirect('user:login')

        # Display any remaining form errors
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(
                    request,
                    f"{field.replace('_', ' ').capitalize()}: {error}"
                )

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

    def form_invalid(self, form):
        """
        Called when login fails. Add an error message.
        """
        messages.error(
            self.request, "Invalid username or password. Please try again."
            )
        return super().form_invalid(form)


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
