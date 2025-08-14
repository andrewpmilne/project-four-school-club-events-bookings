from django.urls import path
from .views import create_enrollment

app_name = 'enrollment'

urlpatterns = [
    path('create/', create_enrollment, name='create_enrollment'),
]
