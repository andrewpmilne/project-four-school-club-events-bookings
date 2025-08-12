from django.contrib import admin
from .models import Child


@admin.register(Child)
class ChildAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'surname', 'parent', 'date_of_birth')
    search_fields = ('first_name', 'surname', 'parent__email', 'parent__name')
