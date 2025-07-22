from django.db import models

class Club(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    min_age = models.PositiveIntegerField()
    max_age = models.PositiveIntegerField()
    capacity = models.PositiveIntegerField()
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return self.name
