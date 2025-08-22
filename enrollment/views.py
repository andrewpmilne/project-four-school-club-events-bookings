from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from user.decorators import role_required
from datetime import date
from .forms import EnrollmentForm
from .models import Enrollment
from club.models import Club


@role_required('parent')
def create_enrollment(request):
    """
    Allows a parent to enroll one of their children into a club.
    Additional server-side validation prevents tampering.
    """
    if request.method == 'POST':
        form = EnrollmentForm(request.POST)

        # Limit child queryset to current user's children
        form.fields['child'].queryset = request.user.children.all()

        if form.is_valid():
            child = form.cleaned_data['child']
            club = form.cleaned_data['club']

            # Extra validation: ensure the child belongs to this parent
            if child.parent != request.user:
                messages.error(
                    request,
                    "You cannot enroll a child that is not yours."
                    )
                return redirect('enrollments:create_enrollment')

            # Extra validation: check if already enrolled
            if Enrollment.objects.filter(child=child, club=club).exists():
                messages.error(
                    request,
                    f"{child.first_name} is already enrolled in {club.name}."
                    )
                return redirect('enrollments:create_enrollment')

            # Extra validation: check age against club limits
            today = date.today()
            age = (
                today.year - child.date_of_birth.year
                - ((today.month, today.day) <
                   (child.date_of_birth.month, child.date_of_birth.day))
            )
            if (
                club.min_age is not None and age < club.min_age
                ) or (
                    club.max_age is not None and age > club.max_age
                    ):
                messages.error(
                    request,
                    f"{child.first_name} does not meet the age "
                    "requirements for {club.name}."
                )
                return redirect('enrollments:create_enrollment')

            # Extra validation: club capacity
            current_enrollments = Enrollment.objects.filter(club=club).count()
            if (
                club.capacity is not None
                and current_enrollments >= club.capacity
            ):
                messages.error(request, f"{club.name} is already full.")
                return redirect('enrollments:create_enrollment')

            # All checks passed: save enrollment
            form.save()
            messages.success(
                request,
                f"{child.first_name} successfully enrolled in {club.name}!")
            return redirect('user:parent_dashboard')
        else:
            messages.error(
                request,
                "Please correct the errors below.")
    else:
        form = EnrollmentForm()
        form.fields['child'].queryset = request.user.children.all()

    return render(request, 'enrollment/create_enrollment.html', {'form': form})


@role_required('parent')
def create_enrollment_with_club(request, club_id):
    """
    Allows a parent to enroll one of their children into a specific club.
    The club field is pre-selected based on the clicked club card.
    """
    # Pre-select the club
    club = get_object_or_404(Club, id=club_id)
    initial_data = {'club': club}

    if request.method == 'POST':
        form = EnrollmentForm(request.POST)
        # Limit child queryset to current user's children
        form.fields['child'].queryset = request.user.children.all()

        if form.is_valid():
            child = form.cleaned_data['child']
            club = form.cleaned_data['club']

            # Ensure child belongs to this parent
            if child.parent != request.user:
                messages.error(
                    request,
                    "You cannot enroll a child that is not yours."
                    )
                return redirect(
                    'enrollments:create_enrollment_with_club',
                    club_id=club.id
                    )

            # Check if already enrolled
            if Enrollment.objects.filter(child=child, club=club).exists():
                messages.error(
                    request,
                    f"{child.first_name} is already enrolled in {club.name}."
                    )
                return redirect(
                    'enrollments:create_enrollment_with_club',
                    club_id=club.id
                    )

            # Check age against club limits
            today = date.today()
            age = today.year - child.date_of_birth.year - (
                (today.month, today.day) <
                (child.date_of_birth.month, child.date_of_birth.day)
            )
            if (club.min_age is not None and age < club.min_age) or \
               (club.max_age is not None and age > club.max_age):
                messages.error(
                    request,
                    f"{child.first_name} does not meet the "
                    "age requirements for {club.name}."
                    )
                return redirect(
                    'enrollments:create_enrollment_with_club',
                    club_id=club.id
                    )

            # Check club capacity
            current_enrollments = Enrollment.objects.filter(club=club).count()
            if (
                club.capacity is not None
                and current_enrollments >= club.capacity
            ):
                messages.error(request, f"{club.name} is already full.")
                return redirect(
                    'enrollments:create_enrollment_with_club',
                    club_id=club.id
                    )

            # All checks passed: save enrollment
            form.save()
            messages.success(
                request,
                f"{child.first_name} successfully enrolled in {club.name}!"
                )
            return redirect('user:parent_dashboard')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = EnrollmentForm(initial=initial_data)
        form.fields['child'].queryset = request.user.children.all()

    return render(request, 'enrollment/create_enrollment.html', {'form': form})
