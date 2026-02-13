# Quickstart Guide: Backend & Data Layer

## Overview
This guide provides instructions for setting up, running, and testing the FastAPI backend for the Todo web application.

## Prerequisites
- Python 3.11+
- Poetry or pip for dependency management
- Neon Serverless PostgreSQL database instance
- Environment variables configured

## Setup Instructions

### 1. Clone and Navigate to Project
```bash
cd backend
```

### 2. Install Dependencies
Using Poetry:
```bash
poetry install
poetry shell
```

Or using pip:
```bash
pip install -r requirements.txt
```

### 3. Environment Configuration
Create a `.env` file in the project root with the following variables:
```env
DATABASE_URL=postgresql+asyncpg://username:password@ep-xxx.us-east-1.aws.neon.tech/dbname
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 4. Database Setup
Run the initial database migration:
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

### Health Check
- `GET /health` - Check if the application is running

### Task Management (User-scoped)
- `GET /api/{user_id}/tasks` - Get all tasks for a user
- `POST /api/{user_id}/tasks` - Create a new task for a user
- `GET /api/{user_id}/tasks/{id}` - Get a specific task
- `PUT /api/{user_id}/tasks/{id}` - Update a specific task
- `DELETE /api/{user_id}/tasks/{id}` - Delete a specific task
- `PATCH /api/{user_id}/tasks/{id}/complete` - Toggle task completion status

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

## Database Migrations
When changing models, create and run migrations:

1. Create migration:
```bash
alembic revision --autogenerate -m "Description of changes"
```

2. Apply migration:
```bash
alembic upgrade head
```

## Example Usage

### Create a Task
```bash
curl -X POST http://localhost:8000/api/1/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Sample Task", "description": "Task description"}'
```

### Get User's Tasks
```bash
curl -X GET http://localhost:8000/api/1/tasks
```

### Update a Task
```bash
curl -X PUT http://localhost:8000/api/1/tasks/1 \
  -H "Content-Type: application/json" \
  -d '{"title": "Updated Task", "description": "Updated description", "completed": false}'
```

## Troubleshooting

### Common Issues
1. **Database Connection Error**: Verify DATABASE_URL in environment variables
2. **Migration Errors**: Run `alembic upgrade head` to ensure database is up to date
3. **Port Already in Use**: Change port in uvicorn command or kill existing process

### Environment Variables
Ensure all required environment variables are set:
- `DATABASE_URL`: Neon PostgreSQL connection string
- `SECRET_KEY`: Secret key for JWT signing
- `ALGORITHM`: Algorithm for JWT encoding
- `ACCESS_TOKEN_EXPIRE_MINUTES`: Token expiration time