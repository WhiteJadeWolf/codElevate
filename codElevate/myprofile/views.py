# myprofile/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Profile
from .forms import UserUpdateForm, ProfileUpdateForm

@login_required
def profile_view(request):
    # Profile is automatically created/retrieved via signal or get_or_create not needed
    # but accessing request.user.profile should work if signals are set up.
    # For safety, you could use get_object_or_404 if signals might fail.
    profile = get_object_or_404(Profile, user=request.user)
    context = {
        'profile': profile,
        'user': request.user
    }
    return render(request, 'myprofile/profile_view.html', context)


@login_required
def profile_edit(request):
    profile = get_object_or_404(Profile, user=request.user)

    if request.method == 'POST':
        # Pass instance=request.user/profile to pre-populate and update
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('myprofile:profile') # Redirect back to profile view page
        else:
            # Pass forms with errors back to template
            messages.error(request, 'Please correct the errors below.')
    else:
        # Populate forms with current data for GET request
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'profile': profile # Pass profile for displaying current picture etc.
    }
    return render(request, 'myprofile/profile_edit.html', context)