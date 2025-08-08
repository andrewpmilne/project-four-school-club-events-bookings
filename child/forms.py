from django import forms
from .models import Child


class ChildForm(forms.ModelForm):
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
