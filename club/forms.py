from django import forms
from .models import Club

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
