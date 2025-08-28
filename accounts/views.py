"""Views to work with profile."""
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect

from .forms import UserForm

User = get_user_model()


@login_required
def profile_details(request, username):
    """Return information about the user."""
    user = get_object_or_404(User, username=username)

    context = {
        'user': user,
    }

    return render(request, 'accounts/profile.html', context)


@login_required
def edit_profile(request):
    """Edit users profile."""
    form = UserForm(request.POST or None, instance=request.user)
    context = {'form': form}

    if form.is_valid():
        form.save()
        return HttpResponseRedirect(
            reverse(
                'accounts:profile',
                kwargs={"username": request.user.username}
            ),
        )

    return render(request, 'accounts/profile.html', context)
