from rest_framework import serializers
from datetime import datetime
from .models import Author, Book

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'publication_year', 'author']


        def validate_publication_year(self, value):
            """Ensure the publication year is not in the future."""
            current_year = datetime.now().year
            if value > current_year:
                raise serializers.validationError("Publication year cannot be in the future.")
            return value
# Represents a writer. Has a one-to-many relationship with Book.
class AuthorSerializer(serializers.ModelSerializer):  # 
    books = BookSerializer(many=True, read_only = True)  # Nested representation
    class Meta:
        model = Author
        fields = ['id', 'name', 'books']
  
