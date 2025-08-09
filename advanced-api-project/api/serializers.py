from rest_framework import serializers
from .models import Author, Book
from datetime import datetime

# BookSerializer serializes all fields of the Book model.
# Includes custom validation to ensure publication_year is not in the future.
class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'publication_year', 'author']

    def validate_publication_year(self, value):
        current_year = datetime.now().year
        if value > current_year:
            raise serializers.ValidationError("Publication year cannot be in the future.")
        return value

# AuthorSerializer serializes the Author model and includes a nested list of books.
# Uses BookSerializer to represent related books dynamically.
class AuthorSerializer(serializers.ModelSerializer):
    books = BookSerializer(many=True, read_only=True)

    class Meta:
        model = Author
        fields = ['id', 'name', 'books']

# The AuthorSerializer uses the related_name 'books' from the Author-Book relationship
# to include all books for a given author as a nested list. This allows for easy
# representation of nested relationships in API responses.