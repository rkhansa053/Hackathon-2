# Data Model: Frontend Web Application

## User Entity
**Representation**: Registered user of the application with authentication credentials and personal task data

**Fields**:
- id: Unique identifier for the user
- email: User's email address (used for authentication)
- createdAt: Timestamp when the user account was created
- updatedAt: Timestamp when the user account was last updated

**Validation Rules**:
- Email must be in valid email format
- Email must be unique across all users
- Email and password required for registration/login

**State Transitions**:
- Unauthenticated → Authenticated (login success)
- Authenticated → Unauthenticated (logout/expired session)

## Task Entity
**Representation**: Todo item belonging to a specific user with properties like title, description, completion status, and timestamps

**Fields**:
- id: Unique identifier for the task
- userId: Reference to the user who owns this task
- title: Short title/description of the task
- description: Optional detailed description of the task
- completed: Boolean indicating whether the task is completed
- createdAt: Timestamp when the task was created
- updatedAt: Timestamp when the task was last updated

**Validation Rules**:
- Title is required (non-empty)
- userId must reference a valid user
- Only the task owner can modify/delete the task
- Completed status can be toggled by the owner

**State Transitions**:
- Pending → Completed (toggle completion)
- Completed → Pending (toggle completion)
- Active → Deleted (delete action)

## Authentication Session
**Representation**: Temporary authenticated session state for a user

**Fields**:
- token: JWT token for authentication
- userId: Reference to the authenticated user
- expiresAt: Expiration timestamp for the token
- createdAt: Timestamp when the session was created

**Validation Rules**:
- Token must be valid and not expired
- Only authenticated users can access protected resources
- Session invalidated on logout

**State Transitions**:
- No session → Active session (successful authentication)
- Active session → No session (logout/expired)

## API Response Types
**Representation**: Structured data types for API communication

**Types**:
- ApiResponse<T>: Generic wrapper for API responses with success/error handling
- AuthResponse: Contains user data and JWT token upon successful authentication
- TaskListResponse: Array of tasks with pagination/metadata
- TaskResponse: Individual task data with full details

**Validation Rules**:
- All API responses follow consistent structure
- Error responses include meaningful error messages
- Success responses include relevant data payload