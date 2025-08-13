from django.contrib import admin
from .models import Club


@admin.register(Club)
class ClubAdmin(admin.ModelAdmin):
    list_display = ('name', 'min_age', 'max_age',
                    'capacity', 'start_time', 'end_time')
    search_fields = ('name',)
    list_filter = ('min_age', 'max_age')
