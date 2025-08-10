from django.urls import path
from .views import create_child, view_children_cards, edit_child, delete_child

app_name = 'child'

urlpatterns = [
    path('create/', create_child, name='create_child'),
    path('view/', view_children_cards, name='view_children_cards'),
    path('edit/<int:child_id>/', edit_child, name='edit_child'),
    path('delete/<int:child_id>/', delete_child, name='delete_child'),
]
