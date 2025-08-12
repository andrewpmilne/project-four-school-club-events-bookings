from django.urls import path
from . import views
from .views import CustomLoginView
from .forms import EmailAuthenticationForm


app_name = 'user'

urlpatterns = [
    path('', views.home_view, name='home'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', CustomLoginView.as_view(
        template_name='user/login.html',
        authentication_form=EmailAuthenticationForm
    ), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/teacher/', views.teacher_dashboard,
         name='teacher_dashboard'),
    path('dashboard/parent/', views.parent_dashboard,
         name='parent_dashboard'),
]
