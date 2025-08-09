from django.db import models

# Author model represents a book author.
# Each author can have multiple books (one-to-many relationship).
class Author(models.Model):
    name = models.CharField(max_length=255, help_text="The author's full name.")

    def __str__(self):
        return self.name

# Book model represents a book written by an author.
# Each book is linked to a single author via a ForeignKey.
class Book(models.Model):
    title = models.CharField(max_length=255, help_text="The title of the book.")
    publication_year = models.IntegerField(help_text="The year the book was published.")
    author = models.ForeignKey(Author, related_name='books', on_delete=models.CASCADE, help_text="The author of the book.")

    def __str__(self):
        return f"{self.title} ({self.publication_year})"

# The Author and Book models are related such that one Author can have many Books.
# This is implemented using a ForeignKey from Book to Author with related_name='books',
# allowing easy access to all books for a given author (e.g., author.books.all()).
