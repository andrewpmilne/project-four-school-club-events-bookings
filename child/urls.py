from django.urls import path
from .views import create_child

app_name = 'child'

urlpatterns = [
    path('create/', create_child, name='create_child'),
]
