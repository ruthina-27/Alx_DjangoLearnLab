# Django REST Framework API Documentation

## Project Overview
This Django REST Framework API provides comprehensive CRUD operations for a book management system with custom serializers, generic views, and permission-based access control.

## Architecture

### Models
- **Author**: Represents book authors with a name field
- **Book**: Represents books with title, publication year, and foreign key to Author

### Serializers
- **BookSerializer**: Handles Book model serialization with custom validation
- **AuthorSerializer**: Handles Author model with nested Book serialization

### Views Implementation
All views are implemented using Django REST Framework's generic views for optimal performance and maintainability.

## API Endpoints

### Book Management

#### 1. List All Books (with Filtering, Searching, and Ordering)
- **URL**: `GET /api/books/`
- **Description**: Retrieve a paginated list of all books with advanced query capabilities
- **Permissions**: Public access (AllowAny)
- **Query Parameters**:
  - **Filtering**: `?title=<title>&author=<author_id>&publication_year=<year>`
  - **Searching**: `?search=<search_term>` (searches title and author name)
  - **Ordering**: `?ordering=title,-publication_year` (prefix with - for descending)
- **Examples**:
  - `GET /api/books/?search=django` - Search for books with "django" in title or author name
  - `GET /api/books/?author=1&publication_year=2023` - Filter by author ID 1 and year 2023
  - `GET /api/books/?ordering=-publication_year` - Order by publication year (newest first)
  - `GET /api/books/?search=python&ordering=title` - Search and order combined
- **Response Format**:
```json
[
  {
    "id": 1,
    "title": "Example Book",
    "publication_year": 2023,
    "author": 1
  }
]
```

#### 2. Book Detail
- **URL**: `GET /api/books/<id>/`
- **Description**: Retrieve detailed information about a specific book
- **Permissions**: Public access (AllowAny)
- **Response Format**:
```json
{
  "id": 1,
  "title": "Example Book",
  "publication_year": 2023,
  "author": 1
}
```

#### 3. Create Book
- **URL**: `POST /api/books/create/`
- **Description**: Create a new book entry
- **Permissions**: Authenticated users only (IsAuthenticated)
- **Request Body**:
```json
{
  "title": "New Book Title",
  "publication_year": 2024,
  "author": 1
}
```
- **Success Response**:
```json
{
  "message": "Book created successfully",
  "data": {
    "id": 2,
    "title": "New Book Title",
    "publication_year": 2024,
    "author": 1
  }
}
```
- **Validation Rules**:
  - Publication year cannot be in the future
  - Title is required and must be non-empty
  - Author must exist in the database

#### 4. Update Book
- **URL**: `PUT /api/books/<id>/update/` or `PATCH /api/books/<id>/update/`
- **Description**: Update an existing book (full or partial update)
- **Permissions**: Authenticated users only (IsAuthenticated)
- **Request Body**: Same as create, but all fields are optional for PATCH
- **Success Response**:
```json
{
  "message": "Book updated successfully",
  "data": {
    "id": 1,
    "title": "Updated Book Title",
    "publication_year": 2024,
    "author": 1
  }
}
```

#### 5. Delete Book
- **URL**: `DELETE /api/books/<id>/delete/`
- **Description**: Remove a book from the database
- **Permissions**: Authenticated users only (IsAuthenticated)
- **Success Response**:
```json
{
  "message": "Book \"Book Title\" has been deleted successfully"
}
```

### Author Management

#### 6. List All Authors
- **URL**: `GET /api/authors/`
- **Description**: Retrieve all authors with their associated books
- **Permissions**: Public access (AllowAny)
- **Response Format**:
```json
[
  {
    "id": 1,
    "name": "Author Name",
    "books": [
      {
        "id": 1,
        "title": "Book Title",
        "publication_year": 2023,
        "author": 1
      }
    ]
  }
]
```

#### 7. Author Detail
- **URL**: `GET /api/authors/<id>/`
- **Description**: Retrieve specific author with nested books
- **Permissions**: Public access (AllowAny)
- **Response Format**: Same as individual item in list view

## View Configurations

### Custom View Behaviors

#### BookCreateView
- **Base Class**: `generics.CreateAPIView`
- **Custom Features**:
  - Enhanced error handling with detailed validation messages
  - Custom response format with success/error indicators
  - Automatic header generation for created resources

#### BookUpdateView  
- **Base Class**: `generics.UpdateAPIView`
- **Custom Features**:
  - Supports both PUT (full update) and PATCH (partial update)
  - Custom validation error handling
  - Detailed success/failure response messages

#### BookDeleteView
- **Base Class**: `generics.DestroyAPIView`
- **Custom Features**:
  - Confirmation message with deleted book title
  - Graceful error handling for non-existent resources

### Permission System

#### Public Endpoints (AllowAny)
- Book List View: Anyone can view the list of books
- Book Detail View: Anyone can view individual book details
- Author List View: Anyone can view authors and their books
- Author Detail View: Anyone can view individual author details

#### Protected Endpoints (IsAuthenticated)
- Book Create View: Only authenticated users can create books
- Book Update View: Only authenticated users can modify books
- Book Delete View: Only authenticated users can delete books

## Validation Rules

### Custom Serializer Validation

#### BookSerializer
- **publication_year**: Must not be in the future
- **title**: Required field, cannot be empty
- **author**: Must reference an existing Author instance

#### AuthorSerializer
- **name**: Required field for author identification
- **books**: Automatically populated via reverse foreign key relationship

## Error Handling

### HTTP Status Codes
- `200 OK`: Successful GET, PUT, PATCH operations
- `201 Created`: Successful POST operations
- `204 No Content`: Successful DELETE operations
- `400 Bad Request`: Validation errors or malformed requests
- `401 Unauthorized`: Missing authentication credentials
- `403 Forbidden`: Authentication required but not provided
- `404 Not Found`: Resource not found
- `405 Method Not Allowed`: HTTP method not supported for endpoint

### Error Response Format
```json
{
  "message": "Validation failed",
  "errors": {
    "field_name": ["Error description"]
  }
}
```

## Testing

### Automated Unit Testing
The API includes comprehensive unit tests in `api/test_views.py` covering:

#### Test Classes
- **BookAPITestCase**: Tests all Book CRUD operations and permissions
- **AuthorAPITestCase**: Tests Author read operations and nested serialization
- **PermissionTestCase**: Comprehensive permission testing for all endpoints
- **FilteringSearchingOrderingTestCase**: Tests advanced query capabilities
- **SerializerValidationTestCase**: Tests custom validation logic

#### Test Coverage (34 Tests)
- ✅ **CRUD Operations**: Create, Read, Update, Delete for all endpoints
- ✅ **Permission Testing**: Authenticated vs unauthenticated access
- ✅ **Filtering**: By title, author, and publication year
- ✅ **Searching**: Full-text search across title and author name
- ✅ **Ordering**: Ascending and descending sort by various fields
- ✅ **Validation**: Custom serializer validation (future publication years)
- ✅ **Error Handling**: 404 errors, validation failures, permission denials
- ✅ **Combined Queries**: Multiple query parameters working together

#### Running Tests
```bash
# Run all API tests
python manage.py test api

# Run specific test class
python manage.py test api.test_views.BookAPITestCase

# Run with verbose output
python manage.py test api --verbosity=2
```

#### Test Results
All 34 tests pass successfully, ensuring:
- API endpoints behave correctly under various conditions
- Permissions are properly enforced
- Data validation works as expected
- Advanced query features function properly

### Manual Testing
The API has also been manually tested using:
- Django's test client for automated endpoint testing
- Permission verification for both authenticated and unauthenticated access
- Validation testing for edge cases (future publication years)
- CRUD operation verification for all endpoints

## Usage Examples

### Authentication
```bash
# Create a user (via Django admin or shell)
python manage.py createsuperuser

# Login is handled via Django's session authentication
# For API clients, use Django REST Framework's authentication mechanisms
```

### cURL Examples

```bash
# List all books
curl -X GET http://localhost:8000/api/books/

# Get specific book
curl -X GET http://localhost:8000/api/books/1/

# Create book (requires authentication)
curl -X POST http://localhost:8000/api/books/create/ \
  -H "Content-Type: application/json" \
  -d '{"title": "New Book", "publication_year": 2024, "author": 1}' \
  --cookie "sessionid=your_session_id"

# Update book (requires authentication)
curl -X PUT http://localhost:8000/api/books/1/update/ \
  -H "Content-Type: application/json" \
  -d '{"title": "Updated Title", "publication_year": 2024, "author": 1}' \
  --cookie "sessionid=your_session_id"

# Delete book (requires authentication)
curl -X DELETE http://localhost:8000/api/books/1/delete/ \
  --cookie "sessionid=your_session_id"
```

## Development Notes

### Generic Views Benefits
- **Reduced Code Duplication**: Standard CRUD operations handled by DRF
- **Built-in Pagination**: Automatic pagination support for list views
- **Consistent Behavior**: Standardized response formats and error handling
- **Extensibility**: Easy to customize via method overrides and mixins

### Security Considerations
- **Permission Classes**: Properly configured for each endpoint
- **Input Validation**: Comprehensive validation at serializer level
- **CSRF Protection**: Handled by Django middleware
- **SQL Injection Prevention**: Automatic via Django ORM

### Performance Optimizations
- **Queryset Optimization**: Efficient database queries via select_related
- **Serializer Caching**: Proper use of read_only fields for nested data
- **Minimal Database Hits**: Strategic use of prefetch_related for nested objects

## Conclusion

This Django REST Framework implementation provides a robust, secure, and well-documented API for book management with the following key features:

1. ✅ **Complete CRUD Operations** for Book model
2. ✅ **Custom Generic Views** with enhanced functionality
3. ✅ **Comprehensive Permission System** for access control
4. ✅ **Custom Validation** for business logic enforcement
5. ✅ **Nested Serialization** for complex data relationships
6. ✅ **Detailed Documentation** for maintainability
7. ✅ **Thorough Testing** for reliability

The API is ready for production use and can be easily extended with additional features such as filtering, searching, and advanced pagination.