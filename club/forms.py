from django import forms
from .models import Club
from django.core.exceptions import ValidationError

class ClubForm(forms.ModelForm):
    class Meta:
        model = Club
        fields = [
            'name',
            'description',
            'min_age',
            'max_age',
            'capacity',
            'start_time',
            'end_time',
            'start_date',
            'end_date',
            'frequency',
        ]
        widgets = {
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'type': 'time'}),
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean(self):
        """
        Perform form-wide validation for ClubForm.
        Adds errors to fields if validation fails.
        """
        # Extracted fields
        name = cleaned_data.get('name')
        frequency = cleaned_data.get('frequency')
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        min_age = cleaned_data.get('min_age')
        max_age = cleaned_data.get('max_age')
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')
        capacity = cleaned_data.get('capacity')

        # Check all fields are filled in
        for field_name in self.fields:
            if cleaned_data.get(field_name) in [None, '']:
                self.add_error(field_name, 'This field is required.')

        # Check club name uniqueness
        if name:
            existing_clubs = Club.objects.filter(name__iexact=name)
            
            if self.instance.pk:
                existing_clubs = existing_clubs.exclude(pk=self.instance.pk)

            if existing_clubs.exists():
                self.add_error('name', 'A club with this name already exists.')

        # Age range validation
        if min_age is not None and max_age is not None:
            if min_age > max_age:
                self.add_error('max_age', 'Maximum age must be greater than or equal to minimum age.')

        # Date range validation
        if start_date and end_date:
            if start_date > end_date:
                self.add_error('end_date', 'End date must be after or equal to start date.')

        # Time range validation
        if start_time and end_time:
            if start_time >= end_time:
                self.add_error('end_time', 'End time must be after start time.')
        
        # One-Off date validation
        if frequency == 'one-off' and start_date != end_date:
            self.add_error('end_date', 'For a One-Off club, start date and end date must be the same.')

        # Capacity validation
        if capacity is not None:
            if capacity <= 0:
                self.add_error('capacity', 'Capacity must be a positive number.')

        return cleaned_data
