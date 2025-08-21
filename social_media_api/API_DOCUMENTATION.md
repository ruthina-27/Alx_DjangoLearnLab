# Social Media API Documentation

## Overview
A Django REST Framework-based social media API that allows users to create accounts, manage posts, and interact through comments.

## Base URL
```
http://localhost:8000/api/
```

## Authentication
The API uses Token-based authentication. Include the token in the Authorization header:
```
Authorization: Token <your-token-here>
```

## Endpoints

### Authentication Endpoints

#### Register User
- **URL**: `/api/accounts/register/`
- **Method**: `POST`
- **Auth Required**: No
- **Data**:
```json
{
    "username": "string",
    "email": "string",
    "password": "string"
}
```
- **Success Response**: `201 Created`
```json
{
    "token": "string"
}
```

#### Login User
- **URL**: `/api/accounts/login/`
- **Method**: `POST`
- **Auth Required**: No
- **Data**:
```json
{
    "username": "string",
    "password": "string"
}
```
- **Success Response**: `200 OK`
```json
{
    "token": "string"
}
```

#### Get User Profile
- **URL**: `/api/accounts/profile/`
- **Method**: `GET`
- **Auth Required**: Yes
- **Success Response**: `200 OK`
```json
{
    "id": 1,
    "username": "string",
    "email": "string",
    "bio": "string",
    "profile_picture": "string"
}
```

### Posts Endpoints

#### List Posts
- **URL**: `/api/posts/`
- **Method**: `GET`
- **Auth Required**: No (read-only)
- **Query Parameters**:
  - `page`: Page number for pagination
  - `search`: Search in title and content
  - `author`: Filter by author ID
  - `ordering`: Order by `created_at`, `updated_at` (use `-` for descending)
- **Success Response**: `200 OK`
```json
{
    "count": 100,
    "next": "http://localhost:8000/api/posts/?page=2",
    "previous": null,
    "results": [
        {
            "id": 1,
            "author": "username",
            "author_id": 1,
            "title": "Post Title",
            "content": "Post content...",
            "created_at": "2023-01-01T12:00:00Z",
            "updated_at": "2023-01-01T12:00:00Z"
        }
    ]
}
```

#### Create Post
- **URL**: `/api/posts/`
- **Method**: `POST`
- **Auth Required**: Yes
- **Data**:
```json
{
    "title": "string",
    "content": "string"
}
```
- **Success Response**: `201 Created`

#### Get Post Detail
- **URL**: `/api/posts/{id}/`
- **Method**: `GET`
- **Auth Required**: No
- **Success Response**: `200 OK`
```json
{
    "id": 1,
    "author": "username",
    "author_id": 1,
    "title": "Post Title",
    "content": "Post content...",
    "created_at": "2023-01-01T12:00:00Z",
    "updated_at": "2023-01-01T12:00:00Z",
    "comments": [
        {
            "id": 1,
            "post": 1,
            "author": "commenter",
            "author_id": 2,
            "content": "Comment content...",
            "created_at": "2023-01-01T12:30:00Z",
            "updated_at": "2023-01-01T12:30:00Z"
        }
    ],
    "comments_count": 1
}
```

#### Update Post
- **URL**: `/api/posts/{id}/`
- **Method**: `PUT` or `PATCH`
- **Auth Required**: Yes (must be author)
- **Data**: Same as create post
- **Success Response**: `200 OK`

#### Delete Post
- **URL**: `/api/posts/{id}/`
- **Method**: `DELETE`
- **Auth Required**: Yes (must be author)
- **Success Response**: `204 No Content`

#### Get Post Comments
- **URL**: `/api/posts/{id}/comments/`
- **Method**: `GET`
- **Auth Required**: No
- **Success Response**: `200 OK` (returns array of comments)

### Comments Endpoints

#### List Comments
- **URL**: `/api/comments/`
- **Method**: `GET`
- **Auth Required**: No
- **Query Parameters**:
  - `page`: Page number for pagination
  - `post`: Filter by post ID
  - `author`: Filter by author ID
  - `ordering`: Order by `created_at`, `updated_at`
- **Success Response**: `200 OK` (paginated response)

#### Create Comment
- **URL**: `/api/comments/`
- **Method**: `POST`
- **Auth Required**: Yes
- **Data**:
```json
{
    "post": 1,
    "content": "string"
}
```
- **Success Response**: `201 Created`

#### Get Comment Detail
- **URL**: `/api/comments/{id}/`
- **Method**: `GET`
- **Auth Required**: No
- **Success Response**: `200 OK`

#### Update Comment
- **URL**: `/api/comments/{id}/`
- **Method**: `PUT` or `PATCH`
- **Auth Required**: Yes (must be author)
- **Data**:
```json
{
    "content": "string"
}
```
- **Success Response**: `200 OK`

#### Delete Comment
- **URL**: `/api/comments/{id}/`
- **Method**: `DELETE`
- **Auth Required**: Yes (must be author)
- **Success Response**: `204 No Content`

## Error Responses

### 400 Bad Request
```json
{
    "field_name": ["Error message"]
}
```

### 401 Unauthorized
```json
{
    "detail": "Authentication credentials were not provided."
}
```

### 403 Forbidden
```json
{
    "detail": "You do not have permission to perform this action."
}
```

### 404 Not Found
```json
{
    "detail": "Not found."
}
```

## Features

### Pagination
- All list endpoints support pagination with 10 items per page
- Use `page` parameter to navigate pages
- Response includes `count`, `next`, and `previous` fields

### Filtering and Search
- **Posts**: Filter by `author`, search in `title` and `content`
- **Comments**: Filter by `post` and `author`
- **Ordering**: Use `ordering` parameter with field names (prefix with `-` for descending)

### Permissions
- **Read access**: Available to all users (authenticated and anonymous)
- **Write access**: Requires authentication
- **Edit/Delete**: Only available to the author of the content

## Setup Instructions

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run migrations:
```bash
python manage.py migrate
```

3. Create superuser (optional):
```bash
python manage.py createsuperuser
```

4. Start development server:
```bash
python manage.py runserver
```

## Testing Examples

### Register and Login
```bash
# Register
curl -X POST http://localhost:8000/api/accounts/register/ \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "email": "test@example.com", "password": "testpass123"}'

# Login
curl -X POST http://localhost:8000/api/accounts/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "password": "testpass123"}'
```

### Create and Manage Posts
```bash
# Create post
curl -X POST http://localhost:8000/api/posts/ \
  -H "Authorization: Token YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title": "My First Post", "content": "This is my first post content."}'

# List posts with search
curl "http://localhost:8000/api/posts/?search=first&ordering=-created_at"

# Get post detail
curl http://localhost:8000/api/posts/1/
```

### Create and Manage Comments
```bash
# Create comment
curl -X POST http://localhost:8000/api/comments/ \
  -H "Authorization: Token YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"post": 1, "content": "Great post!"}'

# List comments for a post
curl "http://localhost:8000/api/comments/?post=1"
```
