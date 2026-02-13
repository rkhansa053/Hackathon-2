# Authentication API Contract

## Overview
Contract defining the authentication API endpoints that the frontend will consume.

## Base URL
`${NEXT_PUBLIC_API_BASE_URL}/api/auth`

## Authentication Endpoints

### POST /signup
Register a new user account.

**Request Body**:
```json
{
  "email": "user@example.com",
  "password": "securePassword123"
}
```

**Response (Success)**:
```json
{
  "success": true,
  "user": {
    "id": "uuid-string",
    "email": "user@example.com",
    "createdAt": "2023-01-01T00:00:00Z"
  },
  "token": "jwt-token-string"
}
```

**Response (Error)**:
```json
{
  "success": false,
  "error": "Descriptive error message"
}
```

**Validation**:
- Email must be in valid email format
- Password must meet minimum strength requirements
- Email must not already exist in the system

### POST /signin
Authenticate an existing user.

**Request Body**:
```json
{
  "email": "user@example.com",
  "password": "securePassword123"
}
```

**Response (Success)**:
```json
{
  "success": true,
  "user": {
    "id": "uuid-string",
    "email": "user@example.com",
    "createdAt": "2023-01-01T00:00:00Z",
    "updatedAt": "2023-01-01T00:00:00Z"
  },
  "token": "jwt-token-string"
}
```

**Response (Error)**:
```json
{
  "success": false,
  "error": "Invalid credentials or other descriptive error message"
}
```

**Validation**:
- Email must exist in the system
- Password must match the stored password for the email
- Account must be active (not suspended)

### GET /profile
Retrieve current user profile (requires authentication).

**Headers**:
```
Authorization: Bearer {jwt-token}
```

**Response (Success)**:
```json
{
  "id": "uuid-string",
  "email": "user@example.com",
  "createdAt": "2023-01-01T00:00:00Z",
  "updatedAt": "2023-01-01T00:00:00Z"
}
```

**Response (Error)**:
```json
{
  "success": false,
  "error": "Unauthorized or other descriptive error message"
}
```

### POST /signout
End the current user session.

**Headers**:
```
Authorization: Bearer {jwt-token}
```

**Response (Success)**:
```json
{
  "success": true,
  "message": "Successfully signed out"
}
```

**Response (Error)**:
```json
{
  "success": false,
  "error": "Sign out failed"
}
```