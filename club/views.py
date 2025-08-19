from django.contrib.auth.decorators import login_required
from user.decorators import role_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from datetime import date

from .models import Club
from .forms import ClubForm


@login_required
@role_required('teacher')
def create_club(request):
    if request.method == 'POST':
        form = ClubForm(request.POST)
        if form.is_valid():
            # Extract raw POST data
            name = request.POST.get('name', '').strip()
            frequency = request.POST.get('frequency')
            start_date = request.POST.get('start_date')
            end_date = request.POST.get('end_date')
            min_age = request.POST.get('min_age')
            max_age = request.POST.get('max_age')
            start_time = request.POST.get('start_time')
            end_time = request.POST.get('end_time')
            capacity = request.POST.get('capacity')

            # Name uniqueness
            if Club.objects.filter(name__iexact=name).exists():
                messages.error(
                    request,
                    'A club with this name already exists.'
                )
                return render(request, 'club/create_club.html', {'form': form})

            # Age validation
            if min_age and max_age and int(min_age) > int(max_age):
                messages.error(
                    request,
                    'Maximum age must be greater than or equal to minimum age.'
                )
                return render(request, 'club/create_club.html', {'form': form})

            # Start date not in past
            if start_date and date.fromisoformat(start_date) < date.today():
                messages.error(request, 'Start date cannot be in the past.')
                return render(request, 'club/create_club.html', {'form': form})

            # Time range validation
            if start_time and end_time and start_time >= end_time:
                messages.error(
                    request,
                    'End time must be after start time.'
                )
                return render(request, 'club/create_club.html', {'form': form})

            # One-off club validation
            if frequency == 'one-off' and start_date != end_date:
                messages.error(
                    request,
                    'For a One-Off club, start and end date must be the same.'
                )
                return render(request, 'club/create_club.html', {'form': form})

            # Capacity validation
            if capacity and int(capacity) <= 0:
                messages.error(
                    request,
                    'Capacity must be a positive number.'
                )
                return render(request, 'club/create_club.html', {'form': form})

            # Save club if all validations pass
            club = form.save(commit=False)
            club.teacher = request.user
            club.save()
            messages.success(request, "Club/Event created successfully!")
            return redirect('user:teacher_dashboard')
    else:
        form = ClubForm()

    return render(request, 'club/create_club.html', {'form': form})


@login_required
@role_required('teacher')
def list_teacher_clubs(request):
    clubs = Club.objects.filter(teacher=request.user).order_by('-created_at')
    return render(request, 'club/list_teacher_clubs.html', {'clubs': clubs})


@login_required
@role_required('teacher')
def manage_single_club(request, club_id):
    club = get_object_or_404(Club, id=club_id, teacher=request.user)

    if request.method == 'POST':
        if 'delete' in request.POST:
            return redirect('club:delete_club_confirm', club_id=club.id)

        form = ClubForm(request.POST, instance=club)
        if form.is_valid():
            # Extract raw POST data
            name = request.POST.get('name', '').strip()
            frequency = request.POST.get('frequency')
            start_date = request.POST.get('start_date')
            end_date = request.POST.get('end_date')
            min_age = request.POST.get('min_age')
            max_age = request.POST.get('max_age')
            start_time = request.POST.get('start_time')
            end_time = request.POST.get('end_time')
            capacity = request.POST.get('capacity')

            # Name uniqueness
            if (
                Club.objects
                .filter(name__iexact=name)
                .exclude(id=club.id)
                .exists()
            ):
                messages.error(
                    request,
                    'A club with this name already exists.'
                )
                return render(
                    request,
                    'club/manage_single_club.html',
                    {'form': form, 'club': club}
                    )

            # Age validation
            if min_age and max_age and int(min_age) > int(max_age):
                messages.error(
                    request,
                    'Maximum age must be greater than or equal to minimum age.'
                )
                return render(
                    request,
                    'club/manage_single_club.html',
                    {'form': form, 'club': club}
                    )

            # Start date not in past
            if start_date and date.fromisoformat(start_date) < date.today():
                messages.error(request, 'Start date cannot be in the past.')
                return render(
                    request,
                    'club/manage_single_club.html',
                    {'form': form, 'club': club}
                    )

            # Time range validation
            if start_time and end_time and start_time >= end_time:
                messages.error(
                    request,
                    'End time must be after start time.'
                )
                return render(
                    request,
                    'club/manage_single_club.html',
                    {'form': form, 'club': club}
                    )

            # One-off club validation
            if frequency == 'one-off' and start_date != end_date:
                messages.error(
                    request,
                    'For a One-Off club, start and end date must be the same.'
                )
                return render(
                    request,
                    'club/manage_single_club.html',
                    {'form': form, 'club': club}
                    )

            # Capacity validation
            if capacity and int(capacity) <= 0:
                messages.error(
                    request,
                    'Capacity must be a positive number.'
                )
                return render(
                    request,
                    'club/manage_single_club.html',
                    {'form': form, 'club': club}
                    )

            # Save club if all validations pass
            form.save()
            messages.success(request, "Club updated successfully.")
            return redirect('club:list_teacher_clubs')
    else:
        form = ClubForm(instance=club)

    return render(
        request,
        'club/manage_single_club.html',
        {'form': form, 'club': club},
    )


@login_required
@role_required('teacher')
def delete_club_confirm(request, club_id):
    club = get_object_or_404(Club, id=club_id, teacher=request.user)
    if request.method == 'POST':
        club.delete()
        messages.success(request, "Club deleted successfully.")
        return redirect('club:list_teacher_clubs')
    return render(request, 'club/delete_club_confirm.html', {'club': club})


@login_required
@role_required('teacher')
def view_club_enrollments(request):
    """
    View all enrollments for clubs managed by the teacher."""
    clubs = (
        Club.objects
        .filter(teacher=request.user)
        .prefetch_related('enrollments__child')
    )
    context = {
        'clubs': clubs
    }
    return render(request, 'club/view_club_enrollments.html', context)
