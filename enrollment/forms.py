from django import forms
from django.core.exceptions import ValidationError
from datetime import date
from .models import Enrollment

class EnrollmentForm(forms.ModelForm):
    class Meta:
        model = Enrollment
        fields = ['child', 'club']
    
    from django.core.exceptions import ValidationError
from datetime import date

class EnrollmentForm(forms.ModelForm):
    class Meta:
        model = Enrollment
        fields = ['child', 'club']

    def clean(self):
        cleaned_data = super().clean()
        child = cleaned_data.get('child')
        club = cleaned_data.get('club')

        if child and club:
            # Calculate age
            today = date.today()
            age = (
                today.year
                - child.date_of_birth.year
                - ((today.month, today.day) < (child.date_of_birth.month, child.date_of_birth.day))
            )

            # Too young
            if club.min_age is not None and age < club.min_age:
                raise ValidationError(
                    f"{child.first_name} {child.surname} is too young for {club.name}. "
                    f"Minimum age is {club.min_age}."
                )

            # Too old
            if club.max_age is not None and age > club.max_age:
                raise ValidationError(
                    f"{child.first_name} {child.surname} is too old for {club.name}. "
                    f"Maximum age is {club.max_age}."
                )

        return cleaned_data
