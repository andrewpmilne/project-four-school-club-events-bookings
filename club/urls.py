from django.urls import path
from .views import create_club, list_teacher_clubs, manage_single_club, delete_club_confirm

app_name = 'club'

urlpatterns = [
    path('create/', create_club, name='create_club'),
    path('my-clubs/', list_teacher_clubs, name='list_teacher_clubs'),
    path('<int:club_id>/', manage_single_club, name='manage_single_club'),
    path('<int:club_id>/delete/', delete_club_confirm, name='delete_club_confirm'),
]
