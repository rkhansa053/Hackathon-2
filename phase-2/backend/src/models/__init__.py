"""
SQLModel models for the Todo application.
All models must be imported here for Alembic autogenerate to discover them.
"""
from .user import User, UserBase, UserCreate, UserUpdate, UserRead
from .task import Task, TaskBase, TaskCreate, TaskUpdate, TaskRead
from .refresh_token import RefreshToken, RefreshTokenBase, RefreshTokenCreate, RefreshTokenRead

__all__ = [
    # User models
    "User",
    "UserBase",
    "UserCreate",
    "UserUpdate",
    "UserRead",
    # Task models
    "Task",
    "TaskBase",
    "TaskCreate",
    "TaskUpdate",
    "TaskRead",
    # RefreshToken models
    "RefreshToken",
    "RefreshTokenBase",
    "RefreshTokenCreate",
    "RefreshTokenRead",
]
