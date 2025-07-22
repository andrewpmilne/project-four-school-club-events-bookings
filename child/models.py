from django.db import models
from django.conf import settings  # to reference your custom user model
from django.utils import timezone

class Child(models.Model):
    parent = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='children')
    name = models.CharField(max_length=255)
    date_of_birth = models.DateField(blank=True, null=True)
    allergy_info = models.TextField(blank=True, null=True)
    emergency_contact_name = models.CharField(max_length=255, blank=True, null=True)
    emergency_contact_phone = models.CharField(max_length=50, blank=True, null=True)
    special_needs = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} (child of {self.parent.name or self.parent.email})"
    
    class Meta:
        verbose_name = "Child"
        verbose_name_plural = "Children"
