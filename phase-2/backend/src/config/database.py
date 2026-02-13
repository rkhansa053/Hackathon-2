from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel
from typing import AsyncGenerator
from .settings import settings


# Create async engine
db_url = settings.database_url
if db_url.startswith("postgresql://"):
    db_url = db_url.replace("postgresql://", "postgresql+asyncpg://", 1)

if db_url.startswith("sqlite"):
    # SQLite specific configuration
    engine = create_async_engine(
        db_url,
        echo=False,  # Set to True for SQL query logging
        connect_args={"check_same_thread": False}  # Required for SQLite
    )
else:
    # PostgreSQL/Neon Serverless configuration
    # Optimized for Neon serverless with connection pooling
    engine = create_async_engine(
        db_url,
        echo=False,  # Set to True for SQL query logging
        pool_pre_ping=True,  # Verify connections before using
        pool_size=10,  # Neon can handle more concurrent connections with pooler
        max_overflow=20,  # Allow burst traffic
        pool_recycle=300,  # Recycle connections every 5 minutes
        pool_timeout=30,  # Wait up to 30 seconds for a connection
        connect_args={
            "server_settings": {
                "application_name": "todo_app",
                "jit": "off",  # Disable JIT for faster cold starts
            },
            "command_timeout": 60,  # Query timeout in seconds
            "timeout": 10,  # Connection timeout in seconds
        },
    )


# Create async session maker
AsyncSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    class_=AsyncSession,
)


async def init_db():
    """Initialize the database and create tables."""
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """Dependency to get async session."""
    async with AsyncSessionLocal() as session:
        yield session