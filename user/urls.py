from django.urls import path
from . import views

app_name = 'user'

urlpatterns = [
    path('', views.home_view, name='home'),
    path('signup/', views.signup_view, name='signup'),
]
