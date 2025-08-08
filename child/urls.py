from django.urls import path
from .views import create_child, view_children_cards

app_name = 'child'

urlpatterns = [
    path('create/', create_child, name='create_child'),
    path('view/', view_children_cards, name='view_children_cards'),
]
