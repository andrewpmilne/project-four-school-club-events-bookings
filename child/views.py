from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from .forms import ChildForm
from .models import Child
from user.decorators import role_required


@login_required
@role_required('parent')
def create_child(request):
    """
    Create a new child record for the logged-in parent.
    """
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
@role_required('parent')
def view_children_cards(request):
    """
    Display all children belonging to the logged-in parent.
    """
    children = Child.objects.filter(parent=request.user)
    return render(
        request,
        'child/view_children_cards.html',
        {
            'children': children,
        }
    )


@login_required
@role_required('parent')
def edit_child(request, child_id):
    """
    View to edit details of a child belonging to the logged-in parent.
    """
    child = get_object_or_404(Child, id=child_id, parent=request.user)

    if request.method == 'POST':
        form = ChildForm(request.POST, instance=child)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                f"{child.first_name} {child.surname}'s "
                "details updated successfully!")
            return redirect('child:view_children_cards')
        else:
            messages.error(request, "Please fix the errors below.")
    else:
        form = ChildForm(instance=child)

    return render(request, 'child/edit_child.html', {
        'form': form,
        'child': child,
    })


@login_required
@role_required('parent')
def delete_child(request, child_id):
    """
    Delete a child belonging to the logged-in parent.
    """
    child = get_object_or_404(Child, id=child_id, parent=request.user)

    if request.method == 'POST':
        child.delete()
        messages.success(
            request, f"{child.first_name} {child.surname} "
            "has been deleted.")
        return redirect('child:view_children_cards')

    return render(request, 'child/delete_child_confirm.html', {'child': child})
