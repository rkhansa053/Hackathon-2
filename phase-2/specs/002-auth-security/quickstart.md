# Quickstart Guide: Auth Security Implementation

## Overview
This guide provides a step-by-step approach to implementing the secure authentication and authorization system using Better Auth and JWT tokens.

## Prerequisites
- Node.js 18+ for frontend development
- Python 3.11+ for backend development
- PostgreSQL database (Neon Serverless recommended)
- Basic understanding of Next.js App Router
- Basic understanding of FastAPI

## Step 1: Install Dependencies

### Frontend (Next.js)
```bash
npm install better-auth @better-fetch/fetch
```

### Backend (FastAPI)
```bash
# Already included in requirements.txt
# Make sure these are in your requirements.txt:
fastapi
python-jose[cryptography]
passlib[bcrypt]
python-multipart
```

## Step 2: Configure Better Auth on Frontend

### Create auth config file
```typescript
// auth.ts
import { betterAuth } from "better-auth";
import { nextCookies, nextHeaders } from "better-auth/integrations/next";

export const auth = betterAuth({
  secret: process.env.BETTER_AUTH_SECRET!,
  baseURL: process.env.NEXT_PUBLIC_APP_URL || "http://localhost:3000",
  appMeta: {
    siteName: "Todo App",
  },
  socialProviders: {
    // Optional: Add Google, GitHub, etc.
  },
  database: {
    // Configure database connection for user sessions
  },
  emailAndPassword: {
    enabled: true,
    requireEmailVerification: false,
  },
  advanced: {
    rateLimit: {
      window: 60000,
      max: 10,
    },
  },
});
```

### Update middleware.ts
```typescript
// middleware.ts
export { auth as middleware } from "@/auth";

export const config = {
  matcher: ["/((?!api|_next/static|_next/image|favicon.ico).*)"],
};
```

## Step 3: Set Up Environment Variables

### Frontend (.env.local)
```
NEXT_PUBLIC_BETTER_AUTH_URL=http://localhost:3000
BETTER_AUTH_SECRET=your-super-secret-key-here
NEXT_PUBLIC_APP_URL=http://localhost:3000
```

### Backend (.env)
```
BETTER_AUTH_SECRET=your-super-secret-key-here
# Make sure this matches the frontend value
```

## Step 4: Create API Client with JWT Integration

### Create auth-aware API client
```typescript
// lib/api-client.ts
import { fetch } from "@better-fetch/fetch";

export const apiClient = fetch("http://localhost:8000", {
  headers: {
    "Content-Type": "application/json",
  },
});

// Wrapper to include auth token
export const authenticatedApiClient = async () => {
  // Get token from Better Auth
  const session = await auth.getSession();

  return fetch("http://localhost:8000", {
    headers: {
      "Content-Type": "application/json",
      "Authorization": `Bearer ${session?.accessToken}`,
    },
  });
};
```

## Step 5: Update FastAPI Backend

### Create JWT verification dependency
```python
# backend/src/api/deps.py
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional
import jwt
from datetime import datetime
from ..config.settings import settings
from ..models.user import User
from sqlmodel import select
from ..config.database import get_async_session
from sqlmodel.ext.asyncio.session import AsyncSession

security = HTTPBearer()

def verify_token(token: str) -> dict:
    """Verify JWT token and return payload."""
    try:
        payload = jwt.decode(
            token,
            settings.secret_key,
            algorithms=[settings.algorithm]
        )
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    session: AsyncSession = Depends(get_async_session)
) -> User:
    """Get current user from JWT token."""
    token = credentials.credentials
    payload = verify_token(token)

    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Fetch user from database
    statement = select(User).where(User.id == user_id)
    result = await session.execute(statement)
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Inactive user",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user
```

## Step 6: Update Task Routes with Auth Enforcement

```python
# backend/src/api/v1/tasks.py (updated)
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import List
from uuid import UUID

from ...schemas.task import TaskCreate, TaskRead, TaskUpdate
from ...services.task_service import TaskService
from ...config.database import get_async_session
from .auth_deps import get_current_user  # Updated import
from ...models.user import User

router = APIRouter()

@router.get("/{user_id}/tasks", response_model=List[TaskRead])
async def get_tasks(
    user_id: str,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session)
):
    """Get all tasks for a specific user."""
    # Verify that the requested user ID matches the current user ID
    try:
        requested_user_id = UUID(user_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid user ID format"
        )

    if current_user.id != requested_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access these tasks"
        )

    task_service = TaskService(session)
    tasks = await task_service.get_tasks_by_user(current_user.id)
    return tasks

# Similar enforcement applies to all other task endpoints
```

## Step 7: Test the Implementation

### Frontend Testing
```bash
# Start the Next.js dev server
npm run dev
```

### Backend Testing
```bash
# Start the FastAPI server
cd backend
python -m uvicorn src.main:app --reload
```

### API Testing
1. Register a new user via Better Auth
2. Verify JWT token is issued
3. Call protected API endpoints with the token
4. Verify that unauthorized access is blocked
5. Verify that cross-user access is blocked

## Security Best Practices Implemented

- JWT tokens with configurable expiration
- Secure token storage using Better Auth
- Proper authorization headers
- User ID verification in route parameters
- Database-level user isolation
- Secure password hashing
- Rate limiting for auth endpoints