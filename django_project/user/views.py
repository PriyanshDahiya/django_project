from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.models import User
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from .forms import UserUpdateForm, ProfileUpdateForm
from .models import Profile

def login(request):
    form = UserCreationForm()
    return render(request, 'user/login.html', {'form': form})

@login_required
def profile(request):
    if request.method == 'POST':
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if p_form.is_valid():
            p_form.save()
            return redirect('profile')
    else:
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'p_form': p_form
    }

    return render(request, 'user/profile.html', context)

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important to update the session with the new password
            messages.success(request, 'Your password has been changed successfully.')
            return redirect('profile')
    else:
        form = PasswordChangeForm(request.user)

    context = {
        'form': form
    }

    return render(request, 'user/change_password.html', context)

def search(request):
    if request.method == 'GET':
        query = request.GET.get('q')
        if query:
            try:
                user = User.objects.get(username=query)
                return redirect('view_profile', username=user.username)
            except User.DoesNotExist:
                pass

    return redirect('home')

def view_profile(request, username):
    user = get_object_or_404(User, username=username)
    is_own_profile = user == request.user

    context = {
        'user': user,
        'is_own_profile': is_own_profile
    }
    return render(request, 'user/view_profile.html', context)
