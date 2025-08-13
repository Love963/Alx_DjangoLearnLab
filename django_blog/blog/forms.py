from django import forms
from .models import Post
from django.contrib.auth.forms import UserCreationForm  # Built-in user registration form with password handling.
from django.contrib.auth.models import User  # User model to create/update users
from .models import Profile   # Import Profile for profile updates

class UserRegisterForm(UserCreationForm):
    # Add email field to the registration field
    email = forms.EmailField(required=True)   # Email is required

    class Meta:
        model = User   # This form creates instances
        # Fields to be included in the form, password1, and password2 come from UserCreationFrom
        fields = ['username', 'email', 'password1', 'password2']

        def clean_email(self):
            # Custom validation for email uniqueness
            email = self.cleaned_data.get('email')  # Get cleaned email data
            if User.objects.filter(email__iexact=email).exits():
                # If a user with this email exists (case-insensitive), raise validation error
                raise forms.ValidationError("A user with that email already exists")
            return email    # Return valid email
class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(required=True)   # Email required when updating profile.

    class Meta:
        model = User  # Update User fields
        fields = ['username', 'email']  # Allow editing username and email
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile   # Update Profile model fields
        fields = ['bio', 'avatar']   # Editable bio and avatar image

class PostForm(forms.ModelForm):
    class Meta:
        model = Post                      # tie form to post model
        fields = ['title', 'content']    # author set in view, not user editable

        widgets = {
            'content': forms.Textarea(attrs={'rows': 8})
        }






