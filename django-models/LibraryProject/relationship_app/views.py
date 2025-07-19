from django.shortcuts import render, get_object_or_404
from django.views.generic.detail import DetailView
from .models import Book, Library

# Function-based view to list all books

def list_books(request):
    """
    This view should render a simple text list of book titles and their authors.
    """
    books = Book.objects.select_related('author').all()
    return render(request, 'list_books.html', {'books': books})

# Class-based view to display details for a specific library
class LibraryDetailView(DetailView):
    """
    Displays details for a specific library, listing all books available in that library.
    Utilizes Django’s DetailView to structure this class-based view.
    """
    model = Library
    template_name = 'library_detail.html'
    context_object_name = 'library'
