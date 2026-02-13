# Data Model: Backend & Data Layer

## Overview
This document defines the data models for the Todo web application backend, focusing on user-scoped task management with proper relationships and constraints.

## Entity: User
**Description**: Represents a registered user in the system

**Fields**:
- `id` (UUID/Integer): Primary key, unique identifier for the user
- `email` (String): User's email address, unique constraint
- `hashed_password` (String): BCrypt hashed password
- `created_at` (DateTime): Timestamp of account creation
- `updated_at` (DateTime): Timestamp of last account update
- `is_active` (Boolean): Account status flag

**Validation Rules**:
- Email must be valid email format
- Email must be unique across all users
- Password must meet minimum security requirements (to be defined)

## Entity: Task
**Description**: Represents a todo item owned by a specific user

**Fields**:
- `id` (UUID/Integer): Primary key, unique identifier for the task
- `title` (String): Task title/description (required)
- `description` (Text, optional): Detailed task description
- `completed` (Boolean): Task completion status, default: False
- `user_id` (UUID/Integer): Foreign key linking to owning user
- `created_at` (DateTime): Timestamp of task creation
- `updated_at` (DateTime): Timestamp of last task update

**Relationships**:
- Task belongs to User (many-to-one)
- User has many Tasks

**Validation Rules**:
- Title must not be empty/null
- User_id must reference an existing, active user
- Completed status can be updated by task owner only

## Database Constraints
1. **Primary Keys**: All entities have unique primary key identifiers
2. **Foreign Key Constraints**: Task.user_id references User.id
3. **Unique Constraints**: User.email must be unique
4. **Not Null Constraints**: Required fields (id, title, user_id, created_at) cannot be null
5. **Check Constraints**: None currently defined, but could add status validation in future

## Indexes
1. **User Table**:
   - Primary key index on `id`
   - Unique index on `email`
   - Index on `created_at` for sorting/filtering

2. **Task Table**:
   - Primary key index on `id`
   - Index on `user_id` for efficient user-based queries
   - Index on `completed` for filtering completed/incomplete tasks
   - Index on `created_at` for chronological ordering
   - Composite index on `(user_id, created_at)` for efficient user timeline queries

## State Transitions
**Task States**:
- Pending → Completed (when user marks task as done)
- Completed → Pending (when user unmarks completed task)

**Transitions**:
- Only the task owner can transition the task state
- State transitions must update the `updated_at` timestamp

## API Representation
**Task Response Schema**:
```
{
  "id": "uuid-string",
  "title": "string",
  "description": "string or null",
  "completed": boolean,
  "user_id": "uuid-string",
  "created_at": "ISO 8601 datetime",
  "updated_at": "ISO 8601 datetime"
}
```

**Task Request Schema**:
```
{
  "title": "string",
  "description": "string or null",
  "completed": boolean
}
```

## Security Considerations
1. All queries must filter by user_id to prevent unauthorized access
2. Write operations must verify user_id matches the authenticated user
3. No direct access to tasks without user context
4. Proper foreign key constraints prevent orphaned tasks