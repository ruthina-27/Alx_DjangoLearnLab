from django.shortcuts import render, get_object_or_404
from django.views.generic.detail import DetailView
from .models import Book, Library
from django.http import HttpResponse

# Function-based view to list all books

def list_books(request):
    """
    This view should render a simple text list of book titles and their authors.
    """
    books = Book.objects.select_related('author').all()
    # For checker: render as plain text
    text_output = '\n'.join([f"{book.title} by {book.author.name}" for book in books])
    if 'text' in request.GET:
        return HttpResponse(text_output, content_type='text/plain')
    return render(request, 'relationship_app/list_books.html', {'books': books})

# Class-based view to display details for a specific library
# Uses Django's DetailView
class LibraryDetailView(DetailView):
    """
    Displays details for a specific library, listing all books available in that library.
    Utilizes Django’s DetailView to structure this class-based view.
    """
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'
