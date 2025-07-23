from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.http import HttpResponse
from django.views.generic.detail import DetailView
from .models import Book, Library, UserProfile

# Book List View (FBV)
def list_books(request):
    books = Book.objects.all()
    return render(request, 'relationship_app/list_books.html', {'books': books})

# Library Detail View (CBV)
class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'

# User Registration View
def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Automatically login after registering
            return redirect('list_books')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

# User Login View
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('list_books')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

# User Logout View
def logout_view(request):
    logout(request)
    return redirect('login')

# Home view (requires login)
@login_required
def home_view(request):
    return HttpResponse("Welcome to the homepage!")

# Role check utility
def role_check(user, role):
    return hasattr(user, 'userprofile') and user.userprofile.role == role

@user_passes_test(lambda u: role_check(u, 'Admin'))
def admin_view(request):
    return render(request, 'relationship_app/admin_view.html')

@user_passes_test(lambda u: role_check(u, 'Librarian'))
def librarian_view(request):
    return render(request, 'relationship_app/librarian_view.html')

@user_passes_test(lambda u: role_check(u, 'Member'))
def member_view(request):
    return render(request, 'relationship_app/member_view.html')
