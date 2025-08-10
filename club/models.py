from django.db import models
from django.conf import settings
from django.utils import timezone

class Club(models.Model):
    FREQUENCY_CHOICES = [
        ('one-off', 'One-Off'),
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
    ]

    teacher = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='clubs')
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    min_age = models.PositiveIntegerField(null=True, blank=True)
    max_age = models.PositiveIntegerField(null=True, blank=True)
    capacity = models.PositiveIntegerField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    frequency = models.CharField(max_length=20, choices=FREQUENCY_CHOICES, default='one-off')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        teacher_name = f"{self.teacher.first_name or ''} {self.teacher.surname or ''}".strip()
        return f"{self.name} (by {teacher_name})"
