from django.urls import path
from .views import create_enrollment, create_enrollment_with_club

app_name = 'enrollment'

urlpatterns = [
    path('create/', create_enrollment, name='create_enrollment'),
    path(
        'create/<int:club_id>/',
        create_enrollment_with_club,
        name='create_enrollment_with_club'
        ),
]
