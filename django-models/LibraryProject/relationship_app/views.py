from django.shortcuts import render
from .models import Book
from django.views.generic.detail import DetailView
from .models import Library

# Create your views here.

# Function-based view to list all books
def list_books_view(request):
    books = Book.objects.all()
    return render(request, 'list_books.html', {'books': books})



# Class-based view to display library details
class LibraryDetailView(DetailView):
    model = Library
    template_name = 'library_detail.html'
    context_object_name = 'library'
