from django.contrib import admin
from .models import Enrollment

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('child', 'club', 'status', 'enrollment_date')
    list_filter = ('status', 'club')
    search_fields = ('child__name', 'club__title')
