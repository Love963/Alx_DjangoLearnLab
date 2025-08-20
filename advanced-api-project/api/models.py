from django.db import models
from django.utils import timezone
# Create your models here.

# Represents a writer. Has a one-to-many relationship with Book.
class Author(models.Model):
    name = models.CharField(max_length=100)    # stores the name of the author

    def __str__(self):
        return self.name 
#  Represents a book. Includes title, publication year, and foreign key to Author.
class Book(models.Model):
    title = models.CharField(max_length=100)  # Title of the book
    publication_year = models.IntegerField()  # Year it was published
    author = models.ForeignKey(Author, related_name='books', on_delete=models.CASCADE)  
      # A ForeignKey creates a one-to-many relationship from Author to Book

    def __str__(self):
        return f"{self.title} ({self.publication_year})"