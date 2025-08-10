from django.urls import path
from .views import create_club

app_name = 'club'

urlpatterns = [
    path('create/', create_club, name='create_club'),
]
