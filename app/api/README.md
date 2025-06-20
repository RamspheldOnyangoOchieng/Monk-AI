# Monk-AI API Documentation

## Overview
The Monk-AI API is built using FastAPI and provides a comprehensive set of endpoints for managing users, projects, code snippets, and code reviews. The API follows RESTful principles and implements proper authentication and authorization mechanisms.

## Directory Structure
```
app/api/
├── routes/
│   ├── users.py      # User management endpoints
│   ├── auth.py       # Authentication endpoints
│   ├── projects.py   # Project management endpoints
│   ├── snippets.py   # Code snippets endpoints
│   ├── reviews.py    # Code reviews endpoints
│   └── __init__.py   # Routes package initialization
├── deps.py           # Dependency injection utilities
├── api.py            # Main APIRouter configuration
└── __init__.py       # API package initialization
```

## Authentication
The API uses JWT (JSON Web Tokens) for authentication. All protected endpoints require a valid JWT token in the Authorization header.

### Authentication Flow
1. User registers via `/auth/register` endpoint
2. User logs in via `/auth/token` endpoint to receive JWT token
3. Token is included in subsequent requests in the Authorization header

## API Endpoints

### Users (`/users`)
- `GET /users/` - List all users (superuser only)
- `POST /users/` - Create new user (superuser only)
- `GET /users/me` - Get current user profile
- `PUT /users/me` - Update current user profile
- `GET /users/{user_id}` - Get specific user
- `PUT /users/{user_id}` - Update specific user (superuser only)
- `DELETE /users/{user_id}` - Delete specific user (superuser only)

### Authentication (`/auth`)
- `POST /auth/token` - Login and get access token
- `POST /auth/register` - Register new user

### Projects (`/projects`)
- `GET /projects/` - List user's projects
- `POST /projects/` - Create new project
- `GET /projects/{project_id}` - Get specific project
- `PUT /projects/{project_id}` - Update project
- `DELETE /projects/{project_id}` - Delete project

### Code Snippets (`/snippets`)
- `GET /snippets/` - List snippets (with optional project filter)
- `POST /snippets/` - Create new snippet
- `GET /snippets/{snippet_id}` - Get specific snippet
- `PUT /snippets/{snippet_id}` - Update snippet
- `DELETE /snippets/{snippet_id}` - Delete snippet

### Code Reviews (`/reviews`)
- `GET /reviews/` - List reviews (with optional snippet filter)
- `POST /reviews/` - Create new review (triggers AI analysis)
- `GET /reviews/{review_id}` - Get specific review
- `PUT /reviews/{review_id}` - Update review
- `DELETE /reviews/{review_id}` - Delete review

## Dependencies
The API uses several key dependencies:
- FastAPI for the web framework
- SQLAlchemy for database operations
- Python-jose for JWT handling
- Passlib and bcrypt for password hashing
- Python-multipart for form data handling

## Security Features
1. JWT-based authentication
2. Password hashing with bcrypt
3. Role-based access control (regular users vs superusers)
4. Resource ownership validation
5. Input validation using Pydantic models

## Error Handling
The API implements consistent error handling with appropriate HTTP status codes:
- 400: Bad Request
- 401: Unauthorized
- 403: Forbidden
- 404: Not Found
- 422: Validation Error

## Background Tasks
The review system implements background tasks for AI analysis:
- Review creation triggers an asynchronous AI analysis
- Results are stored and can be retrieved later

## Best Practices Implemented
1. Type hints throughout the codebase
2. Async/await patterns for better performance
3. Dependency injection for better testability
4. Proper separation of concerns
5. Comprehensive input validation
6. Consistent error handling
7. Clear and descriptive docstrings

## Future Improvements
1. Rate limiting implementation
2. Caching layer for frequently accessed data
3. API versioning strategy
4. Enhanced logging and monitoring
5. WebSocket support for real-time updates
6. Bulk operations for better performance
7. Enhanced search capabilities 