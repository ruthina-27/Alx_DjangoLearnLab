# Social Media API Documentation

## Overview
This is a RESTful API for a social media platform built with Django REST Framework. It includes user authentication, posts, comments, user following system, and personalized feeds.

## Authentication
The API uses Token-based authentication. Include the token in the Authorization header:
```
Authorization: Token your_token_here
```

## Endpoints

### Authentication Endpoints

#### Register
- **URL**: `/api/accounts/register/`
- **Method**: `POST`
- **Body**:
```json
{
    "username": "string",
    "email": "string",
    "password": "string"
}
```
- **Response**: Returns authentication token

#### Login
- **URL**: `/api/accounts/login/`
- **Method**: `POST`
- **Body**:
```json
{
    "username": "string",
    "password": "string"
}
```
- **Response**: Returns authentication token

#### Profile
- **URL**: `/api/accounts/profile/`
- **Method**: `GET`
- **Authentication**: Required
- **Response**: Returns current user's profile information

### User Management Endpoints

#### List Users
- **URL**: `/api/accounts/users/`
- **Method**: `GET`
- **Authentication**: Required
- **Response**: Returns list of all users with follower/following counts

#### User Detail
- **URL**: `/api/accounts/users/{id}/`
- **Method**: `GET`
- **Authentication**: Required
- **Response**: Returns specific user details including follow status

#### Follow User
- **URL**: `/api/accounts/follow/{user_id}/`
- **Method**: `POST`
- **Authentication**: Required
- **Response**: Confirmation message
- **Notes**: Cannot follow yourself or already followed users

#### Unfollow User
- **URL**: `/api/accounts/unfollow/{user_id}/`
- **Method**: `POST`
- **Auth Required**: Yes
- **Success Response**: `200 OK`
```json
{
    "message": "You have unfollowed username"
}
```
- **Error Response**: `400 Bad Request`
```json
{
    "error": "You are not following this user"
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

#### Get Feed
- **URL**: `/api/posts/feed/`
- **Method**: `GET`
- **Auth Required**: Yes
- **Description**: Returns posts from users that the current user follows
- **Success Response**: `200 OK` (paginated response)
```json
{
    "count": 50,
    "next": "http://localhost:8000/api/posts/feed/?page=2",
    "previous": null,
    "results": [
        {
            "id": 1,
            "author": "followed_user",
            "author_id": 2,
            "title": "Post from followed user",
            "content": "This is content from someone I follow",
            "created_at": "2023-01-01T12:00:00Z",
            "updated_at": "2023-01-01T12:00:00Z"
        }
    ]
}
```

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

### Likes and Notifications

#### Like Post
- **URL**: `/api/posts/{id}/like/`
- **Method**: `POST`
- **Auth Required**: Yes
- **Success Response**: `201 Created`
```json
{
    "message": "Post liked successfully"
}
```
- **Notes**: Creates notification for post author (if different user)

#### Unlike Post
- **URL**: `/api/posts/{id}/unlike/`
- **Method**: `POST`
- **Auth Required**: Yes
- **Success Response**: `200 OK`
```json
{
    "message": "Post unliked successfully"
}
```

#### List Notifications
- **URL**: `/api/notifications/`
- **Method**: `GET`
- **Auth Required**: Yes
- **Success Response**: `200 OK`
```json
[
    {
        "id": 1,
        "actor_username": "john_doe",
        "verb": "liked your post",
        "target_type": "post",
        "timestamp": "2023-01-01T12:00:00Z",
        "read": false
    }
]
```

#### Mark Notification as Read
- **URL**: `/api/notifications/{id}/read/`
- **Method**: `POST`
- **Auth Required**: Yes
- **Success Response**: `200 OK`
```json
{
    "message": "Notification marked as read"
}
```

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

### User Following System
- Users can follow and unfollow other users
- User profiles show follower and following counts
- User profiles indicate if the current user is following them
- Feed functionality shows posts from followed users only

### Feed Algorithm
- Feed displays posts from users the current user follows
- Posts are ordered by creation date (most recent first)
- Empty feed if user doesn't follow anyone
- Supports pagination like other endpoints

### Pagination
- All list endpoints support pagination with 10 items per page
- Use `page` parameter to navigate pages
- Response includes `count`, `next`, and `previous` fields

### Filtering and Search
- **Posts**: Filter by `author`, search in `title` and `content`
- **Comments**: Filter by `post` and `author`
- **Users**: Browse all users for discovery
- **Ordering**: Use `ordering` parameter with field names (prefix with `-` for descending)

### Permissions
- **Read access**: Available to all users (authenticated and anonymous)
- **Write access**: Requires authentication
- **Edit/Delete**: Only available to the author of the content
- **Follow/Unfollow**: Requires authentication, users can only modify their own following list

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

# Get personalized feed
curl -H "Authorization: Token YOUR_TOKEN" http://localhost:8000/api/posts/feed/
```

### Follow and Unfollow Users
```bash
# List all users
curl -H "Authorization: Token YOUR_TOKEN" http://localhost:8000/api/accounts/users/

# Get user details
curl -H "Authorization: Token YOUR_TOKEN" http://localhost:8000/api/accounts/users/2/

# Follow a user
curl -X POST -H "Authorization: Token YOUR_TOKEN" http://localhost:8000/api/accounts/follow/2/

# Unfollow a user
curl -X POST -H "Authorization: Token YOUR_TOKEN" http://localhost:8000/api/accounts/unfollow/2/
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
