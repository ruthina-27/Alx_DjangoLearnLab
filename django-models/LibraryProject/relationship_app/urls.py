from django.urls import path
from .views import list_books, LibraryDetailView, LibraryBooksListView

urlpatterns = [
    path('books/', list_books, name='list_books'),  # Function-based view for listing books
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),  # Class-based view for library details
    path('library/<int:pk>/books/', LibraryBooksListView.as_view(), name='library_books_list'),  # Class-based ListView for books in a library
] 