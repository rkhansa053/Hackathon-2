# Tasks API Contract

## Overview
Contract defining the tasks API endpoints that the frontend will consume.

## Base URL
`${NEXT_PUBLIC_API_BASE_URL}/api/tasks`

## Authentication
All endpoints require a valid JWT token in the Authorization header:
```
Authorization: Bearer {jwt-token}
```

## Tasks Endpoints

### GET /?page={page}&limit={limit}
Retrieve the authenticated user's tasks with optional pagination.

**Parameters**:
- `page` (optional): Page number for pagination (default: 1)
- `limit` (optional): Number of tasks per page (default: 10, max: 100)

**Response (Success)**:
```json
{
  "success": true,
  "tasks": [
    {
      "id": "uuid-string",
      "userId": "uuid-string",
      "title": "Task title",
      "description": "Task description (optional)",
      "completed": false,
      "createdAt": "2023-01-01T00:00:00Z",
      "updatedAt": "2023-01-01T00:00:00Z"
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 10,
    "total": 25,
    "hasNext": true,
    "hasPrev": false
  }
}
```

**Response (Error)**:
```json
{
  "success": false,
  "error": "Descriptive error message"
}
```

### POST /
Create a new task for the authenticated user.

**Request Body**:
```json
{
  "title": "New task title",
  "description": "Optional task description",
  "completed": false
}
```

**Response (Success)**:
```json
{
  "success": true,
  "task": {
    "id": "uuid-string",
    "userId": "authenticated-user-id",
    "title": "New task title",
    "description": "Optional task description",
    "completed": false,
    "createdAt": "2023-01-01T00:00:00Z",
    "updatedAt": "2023-01-01T00:00:00Z"
  }
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
- Title must be provided and not empty
- Description length limited to 1000 characters
- Completed field defaults to false if not provided

### GET /{taskId}
Retrieve a specific task by ID for the authenticated user.

**Path Parameter**:
- `taskId`: UUID string of the task to retrieve

**Response (Success)**:
```json
{
  "success": true,
  "task": {
    "id": "uuid-string",
    "userId": "uuid-string",
    "title": "Task title",
    "description": "Task description (optional)",
    "completed": false,
    "createdAt": "2023-01-01T00:00:00Z",
    "updatedAt": "2023-01-01T00:00:00Z"
  }
}
```

**Response (Error)**:
```json
{
  "success": false,
  "error": "Not found or Unauthorized access"
}
```

**Validation**:
- Task must exist
- Task must belong to the authenticated user

### PUT /{taskId}
Update an existing task for the authenticated user.

**Path Parameter**:
- `taskId`: UUID string of the task to update

**Request Body**:
```json
{
  "title": "Updated task title",
  "description": "Updated task description",
  "completed": true
}
```

**Response (Success)**:
```json
{
  "success": true,
  "task": {
    "id": "uuid-string",
    "userId": "uuid-string",
    "title": "Updated task title",
    "description": "Updated task description",
    "completed": true,
    "createdAt": "2023-01-01T00:00:00Z",
    "updatedAt": "2023-01-01T00:00:01Z"
  }
}
```

**Response (Error)**:
```json
{
  "success": false,
  "error": "Not found or Unauthorized access"
}
```

**Validation**:
- Task must exist
- Task must belong to the authenticated user
- At least one field must be provided in the request body

### PATCH /{taskId}/toggle-complete
Toggle the completion status of a task.

**Path Parameter**:
- `taskId`: UUID string of the task to update

**Request Body**: (empty)

**Response (Success)**:
```json
{
  "success": true,
  "task": {
    "id": "uuid-string",
    "userId": "uuid-string",
    "title": "Task title",
    "description": "Task description (optional)",
    "completed": true,
    "createdAt": "2023-01-01T00:00:00Z",
    "updatedAt": "2023-01-01T00:00:01Z"
  }
}
```

**Response (Error)**:
```json
{
  "success": false,
  "error": "Not found or Unauthorized access"
}
```

**Validation**:
- Task must exist
- Task must belong to the authenticated user

### DELETE /{taskId}
Delete a specific task for the authenticated user.

**Path Parameter**:
- `taskId`: UUID string of the task to delete

**Response (Success)**:
```json
{
  "success": true,
  "message": "Task deleted successfully"
}
```

**Response (Error)**:
```json
{
  "success": false,
  "error": "Not found or Unauthorized access"
}
```

**Validation**:
- Task must exist
- Task must belong to the authenticated user