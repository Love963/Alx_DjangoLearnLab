from rest_framework import serializers
from datetime import datetime
from rest_framework.exceptions import ValidationError

from .models import Author, Book

# Serializes all Book fields and validates that publication_year is not in the future.
class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'publication_year', 'author']

    def validate_publication_year(self, value):
        """Ensure the publication year is not in the future."""
        current_year = datetime.now().year
        if value > current_year:
            raise ValidationError("Publication year cannot be in the future.")
        return value

# Serializes the author's name and uses a nested BookSerializer to include related books.
class AuthorSerializer(serializers.ModelSerializer):  # 
    books = BookSerializer(many=True, read_only = True)  # Nested representation
    class Meta:
        model = Author
        fields = ['id', 'name', 'books']
  
