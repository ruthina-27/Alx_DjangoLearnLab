from django.urls import path
from .views import (
    BookListView, BookDetailView, BookCreateView, BookUpdateView, BookDeleteView,
    AuthorListView, AuthorDetailView
)

"""
URL configuration for the API app.

This module defines URL patterns for all API endpoints, mapping specific URLs 
to their corresponding generic views. The URL structure follows REST conventions:

Book endpoints:
- GET /api/books/ : List all books
- GET /api/books/<id>/ : Retrieve a specific book
- POST /api/books/create/ : Create a new book (authenticated users only)
- PUT/PATCH /api/books/<id>/update/ : Update a book (authenticated users only)  
- DELETE /api/books/<id>/delete/ : Delete a book (authenticated users only)

Author endpoints:
- GET /api/authors/ : List all authors with their books
- GET /api/authors/<id>/ : Retrieve a specific author with their books
"""

urlpatterns = [
    # Book CRUD operations
    path('books/', BookListView.as_view(), name='book-list'),
    path('books/<int:pk>/', BookDetailView.as_view(), name='book-detail'),
    path('books/create/', BookCreateView.as_view(), name='book-create'),
    path('books/update/', BookUpdateView.as_view(), name='book-update'),
    path('books/delete/', BookDeleteView.as_view(), name='book-delete'),
    path('books/<int:pk>/update/', BookUpdateView.as_view(), name='book-update-detail'),
    path('books/<int:pk>/delete/', BookDeleteView.as_view(), name='book-delete-detail'),
    
    # Author read operations
    path('authors/', AuthorListView.as_view(), name='author-list'),
    path('authors/<int:pk>/', AuthorDetailView.as_view(), name='author-detail'),
] 