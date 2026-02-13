# Authentication API Documentation

## Overview
This document describes the authentication API endpoints available in the Todo application backend.

## Base URL
`http://localhost:8000/api/v1`

## Authentication Endpoints

### Register User
`POST /api/v1/register`

Registers a new user account.

#### Request Body
```json
{
  "email": "user@example.com",
  "password": "securepassword123"
}
```

#### Response (200 OK)
```json
{
  "email": "user@example.com",
  "id": "uuid-string",
  "created_at": "2026-01-30T10:00:00Z",
  "updated_at": "2026-01-30T10:00:00Z",
  "is_active": true
}
```

#### Error Responses
- `400 Bad Request`: Invalid email format or user already exists
- `422 Unprocessable Entity`: Validation error

### Login User
`POST /api/v1/login`

Authenticates a user and returns access and refresh tokens.

#### Request Body
```json
{
  "email": "user@example.com",
  "password": "securepassword123"
}
```

#### Response (200 OK)
```json
{
  "access_token": "jwt-token-string",
  "refresh_token": "refresh-token-string",
  "token_type": "bearer"
}
```

#### Error Responses
- `401 Unauthorized`: Incorrect email or password
- `422 Unprocessable Entity`: Validation error

### Refresh Access Token
`POST /api/v1/refresh`

Refreshes the access token using a valid refresh token.

#### Request Body
```json
{
  "refresh_token": "refresh-token-string"
}
```

#### Response (200 OK)
```json
{
  "access_token": "new-jwt-token-string",
  "token_type": "bearer"
}
```

#### Error Responses
- `401 Unauthorized`: Invalid or expired refresh token
- `422 Unprocessable Entity`: Validation error

### Logout User
`POST /api/v1/logout`

Logs out the current user and revokes their refresh tokens.

#### Headers
```
Authorization: Bearer {access_token}
```

#### Response (200 OK)
```json
{
  "message": "Logged out successfully. Revoked X refresh tokens."
}
```

#### Error Responses
- `401 Unauthorized`: Invalid or expired access token

## Protected Task Endpoints

All task endpoints require authentication using the `Authorization: Bearer {access_token}` header.

### Get User Tasks
`GET /api/v1/{user_id}/tasks`

Retrieves all tasks for the specified user.

#### Path Parameters
- `user_id`: UUID of the authenticated user

#### Headers
```
Authorization: Bearer {access_token}
```

#### Response (200 OK)
```json
[
  {
    "title": "Task title",
    "description": "Task description",
    "completed": false,
    "id": "uuid-string",
    "user_id": "uuid-string",
    "created_at": "2026-01-30T10:00:00Z",
    "updated_at": "2026-01-30T10:00:00Z"
  }
]
```

#### Error Responses
- `401 Unauthorized`: Missing or invalid access token
- `403 Forbidden`: User ID does not match authenticated user
- `404 Not Found`: User not found

### Create Task
`POST /api/v1/{user_id}/tasks`

Creates a new task for the specified user.

#### Path Parameters
- `user_id`: UUID of the authenticated user

#### Headers
```
Authorization: Bearer {access_token}
```

#### Request Body
```json
{
  "title": "New task",
  "description": "Task description",
  "completed": false
}
```

#### Response (200 OK)
```json
{
  "title": "New task",
  "description": "Task description",
  "completed": false,
  "id": "uuid-string",
  "user_id": "uuid-string",
  "created_at": "2026-01-30T10:00:00Z",
  "updated_at": "2026-01-30T10:00:00Z"
}
```

#### Error Responses
- `401 Unauthorized`: Missing or invalid access token
- `403 Forbidden`: User ID does not match authenticated user
- `404 Not Found`: User not found
- `422 Unprocessable Entity`: Validation error

## Security Headers

All API responses include the following security headers:
- `Strict-Transport-Security`: Enforces HTTPS
- `X-Content-Type-Options`: Prevents MIME type sniffing
- `X-Frame-Options`: Prevents clickjacking
- `X-XSS-Protection`: Enables browser XSS protection
- `Referrer-Policy`: Controls referrer information

## Token Management

- Access tokens expire after 30 minutes (configurable)
- Refresh tokens expire after 7 days (configurable)
- Refresh tokens are rotated on each use
- Logging out revokes all refresh tokens for the user