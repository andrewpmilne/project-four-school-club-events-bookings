from django.db import models

class Club(models.Model):
    FREQUENCY_CHOICES = [
        ('one-off', 'One-Off'),
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
    ]

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    min_age = models.PositiveIntegerField()
    max_age = models.PositiveIntegerField()
    capacity = models.PositiveIntegerField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    frequency = models.CharField(max_length=20, choices=FREQUENCY_CHOICES, default='one-off')

    def __str__(self):
        return self.name
