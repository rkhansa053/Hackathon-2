import re
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import Optional
from uuid import UUID
from datetime import timedelta
from ..models.user import User, UserCreate
from ..utils.security import get_password_hash, verify_password, create_access_token
from fastapi import HTTPException, status


def is_valid_email(email: str) -> bool:
    """Validate email format using regex."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


class AuthService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def register_user(self, user_create: UserCreate) -> User:
        """Register a new user with hashed password."""
        # Validate email format
        if not is_valid_email(user_create.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid email format"
            )

        # Check if user with email already exists
        existing_user = await self.get_user_by_email(user_create.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A user with this email already exists"
            )

        # Hash the password
        hashed_password = get_password_hash(user_create.password)

        # Create new user
        db_user = User(
            email=user_create.email,
            hashed_password=hashed_password
        )

        self.session.add(db_user)
        await self.session.commit()
        await self.session.refresh(db_user)

        return db_user

    async def authenticate_user(self, email: str, password: str) -> Optional[User]:
        """Authenticate user by email and password."""
        # Validate email format
        if not is_valid_email(email):
            return None

        user = await self.get_user_by_email(email)
        if not user or not verify_password(password, user.hashed_password):
            return None
        return user

    async def get_user_by_email(self, email: str) -> Optional[User]:
        """Get user by email."""
        statement = select(User).where(User.email == email)
        result = await self.session.execute(statement)
        return result.scalar_one_or_none()

    async def get_user_by_id(self, user_id: UUID) -> Optional[User]:
        """Get user by ID."""
        statement = select(User).where(User.id == user_id)
        result = await self.session.execute(statement)
        return result.scalar_one_or_none()

    async def create_access_token_for_user(self, user: User) -> str:
        """Create access token for a user."""
        data = {"sub": str(user.id)}
        token = create_access_token(
            data=data,
            expires_delta=timedelta(minutes=30)  # Use default from settings
        )
        return token