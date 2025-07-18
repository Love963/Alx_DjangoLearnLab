import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
django.setup()

from relationship_app.models import Author, Book, Library, Librarian


def query_books_by_author(author_name):
    try:
        author = Author.objects.get(name=author_name)
        books = Book.objects.filter(author=author)
        print(f"\nBooks by {author_name}:")
        for book in books:
            print(f"- {book.title}")
    except Author.DoesNotExist:
        print(f"No author found with name '{author_name}'.")


def list_books_in_library(library_name):
    try:
        library = Library.objects.get(name=library_name)
        books = library.books.all()
        print(f"\nBooks in library '{library_name}':")
        for book in books:
            print(f"- {book.title} by {book.author.name}")
    except Library.DoesNotExist:
        print(f"No library found with name '{library_name}'.")


def get_librarian_for_library(library_name):
    try:
        library = Library.objects.get(name=library_name)
        if hasattr(library, 'librarian'):
            print(f"\nLibrarian for '{library.name}': {library.librarian.name}")
        else:
            print(f"No librarian assigned to '{library_name}'.")
    except Library.DoesNotExist:
        print(f"No library found with name '{library_name}'.")


if __name__ == "__main__":
    query_books_by_author("Tamirat Tezera")
    list_books_in_library("Central Library")
    get_librarian_for_library("Central Library")
