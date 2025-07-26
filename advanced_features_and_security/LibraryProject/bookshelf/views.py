from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import permission_required, login_required
from .models import Book
from django.http import HttpResponseForbidden

# Create your views here.
def book_list(request):
    return render(request, 'bookshelf/book_list.html')  # looks inside templates/bookshelf/

@login_required
@permission_required('book_content.can_view', raise_exception=True)
def view_books(request):
    books = Book.objects.all()
    return render(request, 'book_content/view.books.html', {'books':books})
@login_required
@permission_required('book_content.can_create', raise_exception=True)
def create_book(request):
    if request.method == "POST":
        title = request.POST.get('title')
        content = request.POST.get('content')
        Book.objects.create(title=title, content=content)
        return redirect('view_books')
    return redirect(request, 'book_content.create_book.html')

@login_required
@permission_required('book_content.can_edit', raise_exception=True)
def edit_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method =="POST":
        book.title = request.POST.get('title')
        book.content = request.POST.get('content')
        book.save()
        return redirect('view_books')
    return render(request, 'book_content/edit_book.html', {'book':book})
@login_required
@permission_required('book_content.can_delete', raise_exception=True)
def delete_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == "POST":
        book.delete()
        return redirect('view_books')
    return render(request, 'book_content/delete_book.html', {'book':book})
