from django.contrib.auth.decorators import login_required
from user.decorators import role_required
from django.shortcuts import render, redirect
from django.contrib import messages
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

