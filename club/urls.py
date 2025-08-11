from django.urls import path
from .views import create_club, list_teacher_clubs, manage_single_club

app_name = 'club'

urlpatterns = [
    path('create/', create_club, name='create_club'),
    path('my-clubs/', list_teacher_clubs, name='list_teacher_clubs'),
    path('<int:club_id>/', manage_single_club, name='manage_single_club'),
]
