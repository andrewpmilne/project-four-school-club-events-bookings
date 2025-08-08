from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import ChildForm
from .models import Child
from user.decorators import role_required


@login_required
@role_required('parent')
def create_child(request):
    if request.method == 'POST':
        form = ChildForm(request.POST)
        if form.is_valid():
            child = form.save(commit=False)
            child.parent = request.user
            child.save()
            messages.success(request, "New child created successfully!")
            return redirect('user:parent_dashboard')
    else:
        form = ChildForm()
    return render(request, 'child/create_child.html', {'form': form})


@login_required
def view_children_cards(request):
    children = Child.objects.filter(parent=request.user)
    return render(
        request,
        'child/view_children_cards.html',
        {
            'children': children,
        }
    )
