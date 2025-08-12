from django.db import models
from django.conf import settings
from django.utils import timezone


class Child(models.Model):
    """
    Represents a child linked to a parent (user) in the system.
    """
    parent = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE,
                               related_name='children')
    first_name = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)
    date_of_birth = models.DateField(blank=True, null=True)
    allergy_info = models.TextField(blank=True, null=True)
    emergency_contact_name = models.CharField(max_length=255,
                                              blank=True, null=True)
    emergency_contact_phone = models.CharField(max_length=50,
                                               blank=True, null=True)
    special_needs = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """
        Return a string representation of the child,
        including the parent's name or email.
        """
        parent_name = (
            f"{self.parent.first_name or ''} {self.parent.surname or ''}"
            ).strip()
        if not parent_name:
            parent_name = self.parent.email
        child_full_name = f"{self.first_name} {self.surname}".strip()
        return f"{child_full_name} (child of {parent_name})"

    class Meta:
        verbose_name = "Child"
        verbose_name_plural = "Children"
