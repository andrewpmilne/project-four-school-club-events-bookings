from django.contrib import admin
from .models import Child

@admin.register(Child)
class ChildAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent', 'date_of_birth')
    search_fields = ('name', 'parent__email', 'parent__name')
