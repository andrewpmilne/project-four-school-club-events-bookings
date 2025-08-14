from django.shortcuts import render, redirect
from django.contrib import messages
from user.decorators import role_required
from .forms import EnrollmentForm

@role_required('parent')
def create_enrollment(request):
    """
    Allows a parent to enroll one of their children into a club.
    """
    if request.method == 'POST':
        form = EnrollmentForm(request.POST)
        form.fields['child'].queryset = request.user.children.all()

        if form.is_valid():
            form.save()
            messages.success(request, "Child successfully enrolled!")
            return redirect('user:parent_dashboard')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = EnrollmentForm()
        form.fields['child'].queryset = request.user.children.all()

    return render(request, 'enrollment/create_enrollment.html', {'form': form})
