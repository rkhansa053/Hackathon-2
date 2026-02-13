# Todo Backend API

A FastAPI-based backend for the Todo web application with user authentication and task management.

## Features

- User registration and authentication with JWT tokens
- Secure task management with user isolation
- RESTful API endpoints
- PostgreSQL database with SQLModel ORM
- Password hashing and validation
- User-based data isolation

## Prerequisites

- Python 3.11+
- PostgreSQL database (local or hosted)
- Poetry or pip for dependency management

## Setup

1. Clone the repository
2. Navigate to the backend directory
3. Install dependencies:

Using Poetry:
```bash
poetry install
poetry shell
```

Or using pip:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file based on `.env.example` and configure your database settings:

```env
DATABASE_URL=postgresql+asyncpg://username:password@localhost:5432/todo_db
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

5. Run database migrations:
```bash
alembic upgrade head
```

## Running the Application

### Development
```bash
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

### Production
```bash
uvicorn src.main:app --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

## API Endpoints

### Authentication
- `POST /api/v1/register` - Register a new user
- `POST /api/v1/login` - Login and get JWT token

### Health Check
- `GET /health` - Check if the application is running

### Task Management (Requires Authentication)
- `GET /api/v1/{user_id}/tasks` - Get all tasks for a user
- `POST /api/v1/{user_id}/tasks` - Create a new task for a user
- `GET /api/v1/{user_id}/tasks/{id}` - Get a specific task
- `PUT /api/v1/{user_id}/tasks/{id}` - Update a specific task
- `DELETE /api/v1/{user_id}/tasks/{id}` - Delete a specific task
- `PATCH /api/v1/{user_id}/tasks/{id}/complete` - Toggle task completion status

## Testing

### Run Unit Tests
```bash
pytest tests/unit/
```

### Run Integration Tests
```bash
pytest tests/integration/
```

### Run All Tests
```bash
pytest
```

## Project Structure

```
backend/
├── src/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application entry point
│   ├── config/
│   │   ├── __init__.py
│   │   ├── database.py         # Database configuration and connection
│   │   └── settings.py         # Application settings and environment variables
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py             # User data model
│   │   └── task.py             # Task data model with user relationship
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── user.py             # User request/response schemas
│   │   └── task.py             # Task request/response schemas
│   ├── api/
│   │   ├── __init__.py
│   │   ├── deps.py             # Dependency injection for auth/user context
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── auth.py         # Authentication endpoints
│   │       ├── auth_deps.py    # Authentication dependencies
│   │       └── tasks.py        # Task CRUD endpoints
│   ├── services/
│   │   ├── __init__.py
│   │   ├── auth_service.py     # Authentication business logic
│   │   └── task_service.py     # Task business logic with user isolation
│   └── utils/
│       ├── __init__.py
│       └── security.py         # Security utilities (password hashing, JWT)
├── tests/
│   ├── __init__.py
│   ├── conftest.py             # Test fixtures and configuration
│   ├── unit/
│   │   ├── __init__.py
│   │   ├── test_models/        # Model unit tests
│   │   └── test_schemas/       # Schema validation tests
│   ├── integration/
│   │   ├── __init__.py
│   │   ├── test_auth.py        # Authentication integration tests
│   │   └── test_tasks.py       # Task CRUD integration tests with user isolation
│   └── contract/
│       ├── __init__.py
│       └── test_api_contracts.py # API contract validation tests
├── alembic/
│   ├── versions/               # Database migration files
│   └── env.py                  # Alembic configuration
├── requirements.txt            # Production dependencies
├── requirements-dev.txt        # Development dependencies
└── pyproject.toml              # Project metadata and configuration
```

## Security Features

- JWT-based authentication
- Passwords are hashed using bcrypt
- User isolation - users can only access their own tasks
- Input validation using Pydantic schemas
- SQL injection prevention through parameterized queries

## Environment Variables

- `DATABASE_URL`: PostgreSQL connection string
- `SECRET_KEY`: Secret key for JWT signing
- `ALGORITHM`: Algorithm for JWT encoding
- `ACCESS_TOKEN_EXPIRE_MINUTES`: Token expiration time
- `DEBUG`: Enable/disable debug mode