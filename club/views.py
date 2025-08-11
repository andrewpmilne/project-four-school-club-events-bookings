from django.contrib.auth.decorators import login_required
from user.decorators import role_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Club
from .forms import ClubForm

@login_required
@role_required('teacher')
def create_club(request):
    if request.method == 'POST':
        form = ClubForm(request.POST)
        if form.is_valid():
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
            club.delete()
            messages.success(request, "Club deleted successfully.")
            return redirect('club:list_teacher_clubs')

        form = ClubForm(request.POST, instance=club)
        if form.is_valid():
            form.save()
            messages.success(request, "Club updated successfully.")
            return redirect('club:list_teacher_clubs')
    else:
        form = ClubForm(instance=club)

    return render(request, 'club/manage_single_club.html', {'form': form, 'club': club})