from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .forms import EmailAuthenticationForm

app_name = 'user'


urlpatterns = [
    path('', views.home_view, name='home'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', auth_views.LoginView.as_view(
        template_name='user/login.html',
        authentication_form=EmailAuthenticationForm
    ), name='login'),
]
