from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
import uuid


class UserBase(SQLModel):
    email: str = Field(unique=True, nullable=False, max_length=255)


class User(UserBase, table=True):
    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True)
    hashed_password: str = Field(nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    is_active: bool = Field(default=True)


class UserCreate(UserBase):
    password: str


class UserUpdate(SQLModel):
    email: Optional[str] = None
    password: Optional[str] = None
    is_active: Optional[bool] = None


class UserRead(UserBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime
    is_active: bool