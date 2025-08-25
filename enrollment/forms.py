from django import forms
from django.core.exceptions import ValidationError
from datetime import date
from .models import Enrollment


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
                today.year - child.date_of_birth.year
                - (
                    (today.month, today.day)
                    < (child.date_of_birth.month, child.date_of_birth.day)
                )
            )

            # Too young
            if club.min_age is not None and age < club.min_age:
                raise ValidationError(
                    (
                        f"{child.first_name} {child.surname} is too young "
                        f"for {club.name}. Minimum age is {club.min_age}."
                    )
                )

            # Too old
            if club.max_age is not None and age > club.max_age:
                raise ValidationError(
                    (
                        f"{child.first_name} {child.surname} is too old "
                        f"for {club.name}. Maximum age is {club.max_age}."
                    )
                )

        # Already enrolled
        if Enrollment.objects.filter(child=child, club=club).exists():
            raise ValidationError(
                (
                    f"{child.first_name} {child.surname} is already "
                    f"enrolled in {club.name}."
                )
            )

        # Check if club is full
        current_enrollments = Enrollment.objects.filter(club=club).count()
        if club.capacity is not None and current_enrollments >= club.capacity:
            raise ValidationError(
                (
                    f"{club.name} has reached its maximum capacity of "
                    f"{club.capacity} children."
                )
            )
        
        # Time conflict check
        conflicting_enrollments = Enrollment.objects.filter(
            child=child,
            club__end_date__gte=club.start_date,  # overlap in dates
            club__start_date__lte=club.end_date
        ).exclude(club=club)

        for e in conflicting_enrollments:
            if club.start_time < e.club.end_time and club.end_time > e.club.start_time:
                raise ValidationError(
                    f"{child.first_name} {child.surname} is already enrolled in "
                    f"{e.club.name} which overlaps with {club.name}."
                )

        return cleaned_data
