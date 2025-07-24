from django.db import models
from child.models import Child
from club.models import Club

class Enrollment(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('cancelled', 'Cancelled'),
    ]

    child = models.ForeignKey(Child, on_delete=models.CASCADE, related_name='enrollments')
    club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name='enrollments')
    enrollment_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('child', 'club')  # Prevent double enrollment

    def __str__(self):
        return f"{self.child.name} -> {self.club.name}"
