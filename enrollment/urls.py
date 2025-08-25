from django.urls import path
from .views import (
    create_enrollment,
    create_enrollment_with_club,
    cancel_enrollment,
    cancel_enrollment_page,
)


app_name = 'enrollment'

urlpatterns = [
    path('create/', create_enrollment, name='create_enrollment'),
    path('cancel/', cancel_enrollment_page, name='cancel_enrollment_page'),
    path(
        'cancel/<int:enrollment_id>/',
        cancel_enrollment,
        name='cancel_enrollment'
        ),
    path(
        'create/<int:club_id>/',
        create_enrollment_with_club,
        name='create_enrollment_with_club'
        ),
]
