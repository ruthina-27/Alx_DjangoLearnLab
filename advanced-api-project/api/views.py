from rest_framework import generics, permissions
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Book, Author
from .serializers import BookSerializer, AuthorSerializer

# ListView for retrieving all books
# Allows both authenticated and unauthenticated users to view the list of books
class BookListView(generics.ListAPIView):
    """
    API view to retrieve a list of all books.
    
    - GET /api/books/ : Returns a list of all books
    - Permissions: Read-only access for all users (authenticated and unauthenticated)
    - Serializer: BookSerializer
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]  # Allow read access to everyone

# DetailView for retrieving a single book by ID
# Allows both authenticated and unauthenticated users to view a specific book
class BookDetailView(generics.RetrieveAPIView):
    """
    API view to retrieve a single book by its ID.
    
    - GET /api/books/<id>/ : Returns details of a specific book
    - Permissions: Read-only access for all users (authenticated and unauthenticated)
    - Serializer: BookSerializer
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]  # Allow read access to everyone

# CreateView for adding a new book
# Restricted to authenticated users only
class BookCreateView(generics.CreateAPIView):
    """
    API view to create a new book.
    
    - POST /api/books/create/ : Creates a new book
    - Permissions: Authenticated users only
    - Serializer: BookSerializer with custom validation
    - Custom behavior: Validates data and provides detailed error messages
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]  # Only authenticated users can create
    
    def create(self, request, *args, **kwargs):
        """
        Custom create method with enhanced validation and error handling.
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(
                {
                    'message': 'Book created successfully',
                    'data': serializer.data
                },
                status=status.HTTP_201_CREATED,
                headers=headers
            )
        else:
            return Response(
                {
                    'message': 'Validation failed',
                    'errors': serializer.errors
                },
                status=status.HTTP_400_BAD_REQUEST
            )

# UpdateView for modifying an existing book
# Restricted to authenticated users only
class BookUpdateView(generics.UpdateAPIView):
    """
    API view to update an existing book.
    
    - PUT /api/books/<id>/update/ : Updates all fields of a specific book
    - PATCH /api/books/<id>/update/ : Partially updates a specific book
    - Permissions: Authenticated users only
    - Serializer: BookSerializer with custom validation
    - Custom behavior: Validates data and provides detailed success/error messages
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]  # Only authenticated users can update
    
    def update(self, request, *args, **kwargs):
        """
        Custom update method with enhanced validation and error handling.
        """
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        
        if serializer.is_valid():
            self.perform_update(serializer)
            return Response(
                {
                    'message': 'Book updated successfully',
                    'data': serializer.data
                },
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {
                    'message': 'Validation failed',
                    'errors': serializer.errors
                },
                status=status.HTTP_400_BAD_REQUEST
            )

# DeleteView for removing a book
# Restricted to authenticated users only
class BookDeleteView(generics.DestroyAPIView):
    """
    API view to delete a book.
    
    - DELETE /api/books/<id>/delete/ : Deletes a specific book
    - Permissions: Authenticated users only
    - Custom behavior: Provides confirmation message upon successful deletion
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]  # Only authenticated users can delete
    
    def destroy(self, request, *args, **kwargs):
        """
        Custom destroy method with confirmation message.
        """
        instance = self.get_object()
        book_title = instance.title
        self.perform_destroy(instance)
        return Response(
            {
                'message': f'Book "{book_title}" has been deleted successfully'
            },
            status=status.HTTP_204_NO_CONTENT
        )

# Additional views for Author model (bonus implementation)
class AuthorListView(generics.ListAPIView):
    """
    API view to retrieve a list of all authors with their books.
    
    - GET /api/authors/ : Returns a list of all authors with nested books
    - Permissions: Read-only access for all users
    """
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [permissions.AllowAny]

class AuthorDetailView(generics.RetrieveAPIView):
    """
    API view to retrieve a single author with their books.
    
    - GET /api/authors/<id>/ : Returns details of a specific author with nested books
    - Permissions: Read-only access for all users
    """
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [permissions.AllowAny]
