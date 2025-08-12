from django import forms
from .models import Child
from django.core.exceptions import ValidationError
from datetime import date, timedelta
import re


class ChildForm(forms.ModelForm):
    """
    Form for creating or updating a Child instance.
    """
    class Meta:
        model = Child
        fields = [
            'first_name',
            'surname',
            'date_of_birth',
            'allergy_info',
            'emergency_contact_name',
            'emergency_contact_phone',
            'special_needs',
        ]
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }
    
    def clean(self):
        cleaned_data = super().clean()

        # Extracted fields for validation
        first_name = cleaned_data.get('first_name')
        surname = cleaned_data.get('surname')
        date_of_birth = cleaned_data.get('date_of_birth')
        emergency_phone = cleaned_data.get('emergency_contact_phone')

        # Required fields check
        required_fields = [
            'first_name', 
            'surname', 
            'date_of_birth', 
            'emergency_contact_name', 
            'emergency_contact_phone'
        ]
        for field in required_fields:
            if not cleaned_data.get(field):
                self.add_error(field, 'This field is required.')

        # Age validation: must be between 4 and 18 years old
        if date_of_birth:
            today = date.today()
            age = (today - date_of_birth).days // 365
            if age < 4 or age > 18:
                self.add_error('date_of_birth', 'Child age must be between 4 and 18 years.')

        # Phone number validation
        if emergency_phone:
            phone_pattern = re.compile(r'^\+?[\d\s\-]{7,15}$')
            if not phone_pattern.match(emergency_phone):
                self.add_error('emergency_contact_phone', 'Enter a valid phone number.')
        
        # Check if child already registered (same first_name, surname, dob)
        if first_name and surname and date_of_birth:
            existing_children = Child.objects.filter(
                first_name__iexact=first_name.strip(),
                surname__iexact=surname.strip(),
                date_of_birth=date_of_birth
            )
            # Exclude the current instance if editing
            if self.instance.pk:
                existing_children = existing_children.exclude(pk=self.instance.pk)

            if existing_children.exists():
                self.add_error(None, 'This child is already registered.')

        return cleaned_data