"""
Unit tests for Django REST Framework API views.

This module contains comprehensive test cases for all API endpoints including:
- CRUD operations for Book model
- Filtering, searching, and ordering functionality
- Permission and authentication testing
- Response data integrity and status code verification
"""

from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from .models import Book, Author
from .serializers import BookSerializer, AuthorSerializer


class BookAPITestCase(APITestCase):
    """
    Test cases for Book API endpoints including CRUD operations,
    filtering, searching, ordering, and permission testing.
    """
    
    def setUp(self):
        """
        Set up test data for all test methods.
        Creates test users, authors, and books for testing.
        """
        # Create test users
        self.authenticated_user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        
        # Create test authors
        self.author1 = Author.objects.create(name='John Doe')
        self.author2 = Author.objects.create(name='Jane Smith')
        
        # Create test books
        self.book1 = Book.objects.create(
            title='Django for Beginners',
            publication_year=2020,
            author=self.author1
        )
        self.book2 = Book.objects.create(
            title='Advanced Python Programming',
            publication_year=2021,
            author=self.author2
        )
        self.book3 = Book.objects.create(
            title='REST API Development',
            publication_year=2022,
            author=self.author1
        )
        
        # Set up API client
        self.client = APIClient()
    
    def test_book_list_view_unauthenticated(self):
        """
        Test that unauthenticated users can access the book list.
        """
        url = reverse('book-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 3)  # Paginated response
        
    def test_book_list_view_authenticated(self):
        """
        Test that authenticated users can access the book list.
        """
        self.client.force_authenticate(user=self.authenticated_user)
        url = reverse('book-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 3)
    
    def test_book_detail_view_unauthenticated(self):
        """
        Test that unauthenticated users can access book details.
        """
        url = reverse('book-detail', kwargs={'pk': self.book1.pk})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Django for Beginners')
        self.assertEqual(response.data['author'], self.author1.pk)
    
    def test_book_create_view_authenticated(self):
        """
        Test that authenticated users can create new books.
        """
        self.client.force_authenticate(user=self.authenticated_user)
        url = reverse('book-create')
        data = {
            'title': 'New Test Book',
            'publication_year': 2023,
            'author': self.author1.pk
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'], 'Book created successfully')
        self.assertEqual(response.data['data']['title'], 'New Test Book')
        
        # Verify book was actually created in database
        self.assertTrue(Book.objects.filter(title='New Test Book').exists())
    
    def test_book_create_view_unauthenticated(self):
        """
        Test that unauthenticated users cannot create books.
        """
        url = reverse('book-create')
        data = {
            'title': 'Unauthorized Book',
            'publication_year': 2023,
            'author': self.author1.pk
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_book_create_validation_future_year(self):
        """
        Test that books cannot be created with future publication years.
        """
        self.client.force_authenticate(user=self.authenticated_user)
        url = reverse('book-create')
        data = {
            'title': 'Future Book',
            'publication_year': 2030,  # Future year
            'author': self.author1.pk
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Publication year cannot be in the future', 
                     str(response.data['errors']))
    
    def test_book_update_view_authenticated(self):
        """
        Test that authenticated users can update books.
        """
        self.client.force_authenticate(user=self.authenticated_user)
        url = reverse('book-update-detail', kwargs={'pk': self.book1.pk})
        data = {
            'title': 'Updated Django Book',
            'publication_year': 2021,
            'author': self.author1.pk
        }
        response = self.client.put(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Book updated successfully')
        self.assertEqual(response.data['data']['title'], 'Updated Django Book')
        
        # Verify book was actually updated in database
        updated_book = Book.objects.get(pk=self.book1.pk)
        self.assertEqual(updated_book.title, 'Updated Django Book')
    
    def test_book_update_view_unauthenticated(self):
        """
        Test that unauthenticated users cannot update books.
        """
        url = reverse('book-update-detail', kwargs={'pk': self.book1.pk})
        data = {'title': 'Unauthorized Update'}
        response = self.client.put(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_book_delete_view_authenticated(self):
        """
        Test that authenticated users can delete books.
        """
        self.client.force_authenticate(user=self.authenticated_user)
        url = reverse('book-delete-detail', kwargs={'pk': self.book1.pk})
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertIn('Django for Beginners', response.data['message'])
        
        # Verify book was actually deleted from database
        self.assertFalse(Book.objects.filter(pk=self.book1.pk).exists())
    
    def test_book_delete_view_unauthenticated(self):
        """
        Test that unauthenticated users cannot delete books.
        """
        url = reverse('book-delete-detail', kwargs={'pk': self.book1.pk})
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_book_filtering_by_author(self):
        """
        Test filtering books by author.
        """
        url = reverse('book-list')
        response = self.client.get(url, {'author': self.author1.pk})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Should return 2 books by author1 (book1 and book3)
        self.assertEqual(len(response.data['results']), 2)
        
        # Verify all returned books are by the correct author
        for book in response.data['results']:
            self.assertEqual(book['author'], self.author1.pk)
    
    def test_book_filtering_by_publication_year(self):
        """
        Test filtering books by publication year.
        """
        url = reverse('book-list')
        response = self.client.get(url, {'publication_year': 2021})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['publication_year'], 2021)
    
    def test_book_search_functionality(self):
        """
        Test search functionality across title and author name.
        """
        url = reverse('book-list')
        
        # Search by title
        response = self.client.get(url, {'search': 'Django'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertIn('Django', response.data['results'][0]['title'])
        
        # Search by author name
        response = self.client.get(url, {'search': 'John'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)  # 2 books by John Doe
    
    def test_book_ordering_functionality(self):
        """
        Test ordering functionality for books.
        """
        url = reverse('book-list')
        
        # Order by title (ascending)
        response = self.client.get(url, {'ordering': 'title'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        titles = [book['title'] for book in response.data['results']]
        self.assertEqual(titles, sorted(titles))
        
        # Order by publication year (descending)
        response = self.client.get(url, {'ordering': '-publication_year'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        years = [book['publication_year'] for book in response.data['results']]
        self.assertEqual(years, sorted(years, reverse=True))
    
    def test_book_combined_filtering_search_ordering(self):
        """
        Test combined filtering, searching, and ordering.
        """
        url = reverse('book-list')
        response = self.client.get(url, {
            'search': 'John',  # Search for books by John Doe
            'ordering': '-publication_year'  # Order by year descending
        })
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)
        
        # Verify ordering (REST API Development should come first - 2022)
        self.assertEqual(response.data['results'][0]['title'], 'REST API Development')
        self.assertEqual(response.data['results'][1]['title'], 'Django for Beginners')
    
    def test_book_create_missing_required_fields(self):
        """
        Test that creating a book without required fields fails.
        """
        self.client.force_authenticate(user=self.authenticated_user)
        url = reverse('book-create')
        data = {
            'publication_year': 2023
            # Missing title and author
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('errors', response.data)
    
    def test_book_update_partial(self):
        """
        Test partial update (PATCH) of a book.
        """
        self.client.force_authenticate(user=self.authenticated_user)
        url = reverse('book-update-detail', kwargs={'pk': self.book1.pk})
        data = {'title': 'Partially Updated Title'}
        response = self.client.patch(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['data']['title'], 'Partially Updated Title')
        # Verify other fields remain unchanged
        self.assertEqual(response.data['data']['publication_year'], 2020)
    
    def test_book_delete_nonexistent(self):
        """
        Test deleting a non-existent book returns 404.
        """
        self.client.force_authenticate(user=self.authenticated_user)
        url = reverse('book-delete-detail', kwargs={'pk': 9999})
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_book_detail_nonexistent(self):
        """
        Test retrieving a non-existent book returns 404.
        """
        url = reverse('book-detail', kwargs={'pk': 9999})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class AuthorAPITestCase(APITestCase):
    """
    Test cases for Author API endpoints.
    """
    
    def setUp(self):
        """
        Set up test data for author tests.
        """
        self.author = Author.objects.create(name='Test Author')
        self.book = Book.objects.create(
            title='Test Book',
            publication_year=2023,
            author=self.author
        )
        self.client = APIClient()
    
    def test_author_list_view(self):
        """
        Test retrieving list of authors with nested books.
        """
        url = reverse('author-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Find our test author in the paginated response
        test_author = next((author for author in response.data['results'] if author['name'] == 'Test Author'), None)
        self.assertIsNotNone(test_author)
        self.assertEqual(len(test_author['books']), 1)
        self.assertEqual(test_author['books'][0]['title'], 'Test Book')
    
    def test_author_detail_view(self):
        """
        Test retrieving specific author with nested books.
        """
        url = reverse('author-detail', kwargs={'pk': self.author.pk})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Test Author')
        self.assertEqual(len(response.data['books']), 1)
        self.assertEqual(response.data['books'][0]['title'], 'Test Book')


class PermissionTestCase(APITestCase):
    """
    Comprehensive permission testing for all API endpoints.
    """
    
    def setUp(self):
        """
        Set up test data for permission tests.
        """
        self.user = User.objects.create_user(
            username='permissionuser',
            password='testpass123'
        )
        self.author = Author.objects.create(name='Permission Test Author')
        self.book = Book.objects.create(
            title='Permission Test Book',
            publication_year=2023,
            author=self.author
        )
        self.client = APIClient()
    
    def test_read_permissions_unauthenticated(self):
        """
        Test that read operations are allowed for unauthenticated users.
        """
        # Test book list
        response = self.client.get(reverse('book-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Test book detail
        response = self.client.get(reverse('book-detail', kwargs={'pk': self.book.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Test author list
        response = self.client.get(reverse('author-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Test author detail
        response = self.client.get(reverse('author-detail', kwargs={'pk': self.author.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_write_permissions_unauthenticated(self):
        """
        Test that write operations are denied for unauthenticated users.
        """
        # Test create
        response = self.client.post(reverse('book-create'), {
            'title': 'Unauthorized Book',
            'publication_year': 2023,
            'author': self.author.pk
        })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        # Test update
        response = self.client.put(reverse('book-update-detail', kwargs={'pk': self.book.pk}), {
            'title': 'Unauthorized Update'
        })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        # Test delete
        response = self.client.delete(reverse('book-delete-detail', kwargs={'pk': self.book.pk}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_write_permissions_authenticated(self):
        """
        Test that write operations are allowed for authenticated users.
        """
        self.client.force_authenticate(user=self.user)
        
        # Test create
        response = self.client.post(reverse('book-create'), {
            'title': 'Authorized Book',
            'publication_year': 2023,
            'author': self.author.pk
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Test update
        response = self.client.put(reverse('book-update-detail', kwargs={'pk': self.book.pk}), {
            'title': 'Authorized Update',
            'publication_year': 2023,
            'author': self.author.pk
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class FilteringSearchingOrderingTestCase(APITestCase):
    """
    Comprehensive tests for filtering, searching, and ordering functionality.
    """
    
    def setUp(self):
        """
        Set up test data for filtering, searching, and ordering tests.
        """
        # Create multiple authors and books for comprehensive testing
        self.author_python = Author.objects.create(name='Python Expert')
        self.author_django = Author.objects.create(name='Django Master')
        self.author_web = Author.objects.create(name='Web Developer')
        
        # Create books with varied data for testing
        Book.objects.create(title='Python Basics', publication_year=2020, author=self.author_python)
        Book.objects.create(title='Advanced Python', publication_year=2022, author=self.author_python)
        Book.objects.create(title='Django Fundamentals', publication_year=2021, author=self.author_django)
        Book.objects.create(title='Django Advanced', publication_year=2023, author=self.author_django)
        Book.objects.create(title='Web Development', publication_year=2019, author=self.author_web)
        
        self.client = APIClient()
    
    def test_filtering_by_title(self):
        """
        Test filtering books by exact title match.
        """
        url = reverse('book-list')
        response = self.client.get(url, {'title': 'Python Basics'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['title'], 'Python Basics')
    
    def test_filtering_by_author(self):
        """
        Test filtering books by author ID.
        """
        url = reverse('book-list')
        response = self.client.get(url, {'author': self.author_python.pk})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)  # 2 Python books
        
        for book in response.data['results']:
            self.assertEqual(book['author'], self.author_python.pk)
    
    def test_filtering_by_publication_year(self):
        """
        Test filtering books by publication year.
        """
        url = reverse('book-list')
        response = self.client.get(url, {'publication_year': 2022})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['title'], 'Advanced Python')
    
    def test_search_by_title(self):
        """
        Test searching books by title content.
        """
        url = reverse('book-list')
        response = self.client.get(url, {'search': 'Django'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)  # 2 Django books
        
        for book in response.data['results']:
            self.assertIn('Django', book['title'])
    
    def test_search_by_author_name(self):
        """
        Test searching books by author name.
        """
        url = reverse('book-list')
        response = self.client.get(url, {'search': 'Expert'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)  # 2 books by Python Expert
    
    def test_ordering_by_title_ascending(self):
        """
        Test ordering books by title in ascending order.
        """
        url = reverse('book-list')
        response = self.client.get(url, {'ordering': 'title'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        titles = [book['title'] for book in response.data['results']]
        self.assertEqual(titles, sorted(titles))
    
    def test_ordering_by_publication_year_descending(self):
        """
        Test ordering books by publication year in descending order.
        """
        url = reverse('book-list')
        response = self.client.get(url, {'ordering': '-publication_year'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        years = [book['publication_year'] for book in response.data['results']]
        self.assertEqual(years, sorted(years, reverse=True))
    
    def test_combined_filter_search_order(self):
        """
        Test combining filtering, searching, and ordering in one request.
        """
        url = reverse('book-list')
        response = self.client.get(url, {
            'search': 'Python',
            'ordering': '-publication_year'
        })
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)
        
        # Verify ordering (Advanced Python 2022 should come before Python Basics 2020)
        self.assertEqual(response.data['results'][0]['title'], 'Advanced Python')
        self.assertEqual(response.data['results'][1]['title'], 'Python Basics')


class SerializerValidationTestCase(APITestCase):
    """
    Test cases for custom serializer validation.
    """
    
    def setUp(self):
        """
        Set up test data for serializer validation tests.
        """
        self.user = User.objects.create_user(username='validationuser', password='testpass123')
        self.author = Author.objects.create(name='Validation Author')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
    
    def test_publication_year_validation_future(self):
        """
        Test that future publication years are rejected.
        """
        url = reverse('book-create')
        data = {
            'title': 'Future Book',
            'publication_year': 2030,
            'author': self.author.pk
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Publication year cannot be in the future', 
                     str(response.data['errors']))
    
    def test_publication_year_validation_valid(self):
        """
        Test that current and past publication years are accepted.
        """
        url = reverse('book-create')
        data = {
            'title': 'Valid Book',
            'publication_year': 2023,
            'author': self.author.pk
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['data']['publication_year'], 2023)
