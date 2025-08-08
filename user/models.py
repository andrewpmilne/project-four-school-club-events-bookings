from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils import timezone

class UserManager(BaseUserManager):
    """
    Custom manager for the User model with methods to create users and superusers.
    """
    def create_user(self, email, password, role, first_name=None, surname=None, **extra_fields):
        """
        Create and return a regular user with the given email, password, and role.
        """
        if not email:
            raise ValueError('Users must have an email address')
        if role not in ('teacher', 'parent'):
            raise ValueError('Role must be either "teacher" or "parent"')

        email = self.normalize_email(email)
        user = self.model(email=email, role=role, first_name=first_name, surname=surname, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, role='teacher', first_name=None, surname=None, **extra_fields):
        """
        Create and return a superuser with the given email, password, and role.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, role, first_name, surname, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom User model supporting 'teacher' and 'parent' roles,
    using email as the unique identifier for authentication.
    """
    ROLE_CHOICES = [
        ('teacher', 'Teacher'),
        ('parent', 'Parent'),
    ]

    id = models.AutoField(primary_key=True)
    email = models.EmailField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255, blank=True, null=True)
    surname = models.CharField(max_length=255, blank=True, null=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['role'] 

    def __str__(self):
        """
        Return a string representation of the user.
        """
        return self.email
