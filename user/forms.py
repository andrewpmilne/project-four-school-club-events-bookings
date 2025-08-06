import re
from django import forms
from user.models import User
from django.contrib.auth.forms import AuthenticationForm

class SignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['email', 'first_name', 'surname', 'role']

    # validation for the signup form
    def clean(self):
        cleaned_data = super().clean()

        # Check for required fields
        required_fields = ['email', 'first_name', 'surname', 'role', 'password', 'password_confirm']
        for field in required_fields:
            value = cleaned_data.get(field)
            if not value or (isinstance(value, str) and value.strip() == ''):
                self.add_error(field, f"{field.replace('_', ' ').capitalize()} is required.")
        
        # Email domain validation for teachers
        role = cleaned_data.get('role')
        email = cleaned_data.get('email')
        if role == 'teacher':
            if email and not email.endswith('.sch.uk'):
                self.add_error('email', "Teachers must sign up with an email address ending in '.sch.uk'.")

        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')
        
        # Password validation
        if password and password_confirm:
            if password != password_confirm:
                raise forms.ValidationError("Passwords do not match.")
            if len(password) < 8:
                raise forms.ValidationError("Password must be at least 8 characters long.")
            if not re.search(r'[A-Z]', password):
                raise forms.ValidationError("Password must contain at least one uppercase letter.")
            if not re.search(r'\d', password):
                raise forms.ValidationError("Password must contain at least one number.")
            if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
                raise forms.ValidationError("Password must contain at least one special character.")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user

class EmailAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'autofocus': True}))