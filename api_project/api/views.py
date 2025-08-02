from django.shortcuts import render
from rest_framework import generics, viewsets, permissions
from .models import Book
from .serializers import BookSerializer

# Create your views here.

class BookList(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    # Authentication and Permissions Documentation:
    # - TokenAuthentication: Users must provide a valid token in the Authorization header
    # - IsAuthenticated: Only authenticated users can access these endpoints
    # - To obtain a token, POST to /api-token-auth/ with username and password
    # - Use the token in requests: Authorization: Token <your_token_here>
