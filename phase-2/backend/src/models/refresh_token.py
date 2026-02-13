from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
import uuid


class RefreshTokenBase(SQLModel):
    user_id: uuid.UUID = Field(nullable=False)
    expires_at: datetime = Field(nullable=False)
    revoked: bool = Field(default=False)


class RefreshToken(RefreshTokenBase, table=True):
    """Model for refresh tokens with rotation support."""
    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True)
    token_hash: str = Field(nullable=False)  # Hashed refresh token
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class RefreshTokenCreate(RefreshTokenBase):
    token_hash: str


class RefreshTokenRead(RefreshTokenBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime