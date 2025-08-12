from django.shortcuts import render, redirect  # For rendering templates and redirecting
from django.contrib import messages   # Django's framework for flash notifications
from django.contrib.auth.decorators import login_required  # Restrict views to-logged in users
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm   # Import our custom forms



# Create your views here.
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)  # Bind form with POST data
        if form.is_valid():  # Validate form data
            user = form.save()  # Save new User (handles password hashing)
            username = form.cleaned_data.get('username')  # Get username for message
            messages.success(request, f'Account created for {username}. You can log in now.')  # Flash success message
            return redirect('login')  # Redirect to login page after successful registration
    else:
        form = UserRegisterForm()  # Instantiate empty form for GET request
    return render(request, 'blog/register.html', {'form': form})  # Render registration page with form

@login_required  # User must be logged in to access this view
def profile(request):
    if request.method == 'POST':
        # Bind forms with POST data and files, linked to current user instances
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():  # Validate both forms
            u_form.save()  # Save updated user info
            p_form.save()  # Save updated profile info (including avatar)
            messages.success(request, 'Your profile was updated successfully.')  # Flash success message
            return redirect('profile')  # Redirect to profile page to prevent resubmission
    else:
        # For GET requests, pre-populate forms with current user data
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {'u_form': u_form, 'p_form': p_form}  # Context dictionary to pass to template
    return render(request, 'blog/profile.html', context)  # Render profile page with forms
    




