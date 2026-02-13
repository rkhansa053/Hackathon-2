from typing import AsyncGenerator
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import Depends, HTTPException, status
from ..config.database import get_async_session
import uuid


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """Dependency to get database session."""
    async for session in get_async_session():
        try:
            yield session
        finally:
            await session.aclose()


def get_current_user_id(user_id: str) -> uuid.UUID:
    """Extract and validate user ID from path parameter."""
    try:
        return uuid.UUID(user_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid user ID format"
        )