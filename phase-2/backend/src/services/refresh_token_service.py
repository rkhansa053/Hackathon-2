from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import Optional
import uuid
from datetime import datetime, timedelta
from passlib.context import CryptContext

from ..models.refresh_token import RefreshToken, RefreshTokenCreate
from ..utils.security import create_refresh_token


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class RefreshTokenService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_refresh_token(self, user_id: uuid.UUID) -> tuple[RefreshToken, str]:
        """Create a new refresh token for a user and return both the token and plain token string."""
        # Generate a random token
        import secrets
        plain_token = secrets.token_urlsafe(32)

        # Hash the token for storage
        token_hash = pwd_context.hash(plain_token)

        # Create refresh token record
        refresh_token_data = RefreshTokenCreate(
            user_id=user_id,
            token_hash=token_hash,
            expires_at=datetime.utcnow() + timedelta(days=7)  # 7 days expiration
        )

        db_token = RefreshToken(
            user_id=refresh_token_data.user_id,
            token_hash=refresh_token_data.token_hash,
            expires_at=refresh_token_data.expires_at
        )

        self.session.add(db_token)
        await self.session.commit()
        await self.session.refresh(db_token)

        return db_token, plain_token

    async def verify_refresh_token(self, plain_token: str, user_id: uuid.UUID) -> Optional[RefreshToken]:
        """Verify a refresh token belongs to the user and is valid."""
        # Get all refresh tokens for the user
        statement = select(RefreshToken).where(
            RefreshToken.user_id == user_id,
            RefreshToken.revoked == False,
            RefreshToken.expires_at > datetime.utcnow()
        )
        result = await self.session.execute(statement)
        tokens = result.scalars().all()

        # Check if the provided token matches any valid token for the user
        for token in tokens:
            if pwd_context.verify(plain_token, token.token_hash):
                return token

        return None

    async def revoke_refresh_token(self, token_id: uuid.UUID) -> bool:
        """Revoke a refresh token."""
        statement = select(RefreshToken).where(RefreshToken.id == token_id)
        result = await self.session.execute(statement)
        token = result.scalar_one_or_none()

        if token:
            token.revoked = True
            self.session.add(token)
            await self.session.commit()
            return True

        return False

    async def revoke_all_user_tokens(self, user_id: uuid.UUID) -> int:
        """Revoke all refresh tokens for a user."""
        statement = select(RefreshToken).where(
            RefreshToken.user_id == user_id,
            RefreshToken.revoked == False
        )
        result = await self.session.execute(statement)
        tokens = result.scalars().all()

        revoked_count = 0
        for token in tokens:
            token.revoked = True
            self.session.add(token)
            revoked_count += 1

        if revoked_count > 0:
            await self.session.commit()

        return revoked_count