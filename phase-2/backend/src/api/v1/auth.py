from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import Dict
from uuid import UUID
import secrets
from pydantic import BaseModel

from ...schemas.user import UserCreate, UserRead, UserLogin, UserRegisterResponse
from ...services.auth_service import AuthService
from ...config.database import get_async_session
from ...models.user import User
from ...models.refresh_token import RefreshToken
from ...services.refresh_token_service import RefreshTokenService
from ...utils.security import create_access_token, verify_token
from ...api.v1.auth_deps import get_current_user
from sqlmodel import select


router = APIRouter()


@router.post("/register", response_model=UserRegisterResponse)
async def register_user(
    user_create: UserCreate,
    session: AsyncSession = Depends(get_async_session)
):
    """Register a new user."""
    auth_service = AuthService(session)
    try:
        # Register user
        db_user = await auth_service.register_user(user_create)

        # Create access token
        access_token = await auth_service.create_access_token_for_user(db_user)

        # Create refresh token
        refresh_token_service = RefreshTokenService(session)
        refresh_token_record, plain_refresh_token = await refresh_token_service.create_refresh_token(db_user.id)
        composite_refresh_token = f"{db_user.id}:{plain_refresh_token}"

        return {
            "user": db_user,
            "access_token": access_token,
            "refresh_token": composite_refresh_token,
            "token_type": "bearer"
        }
    except HTTPException:
        # Re-raise HTTP exceptions from auth service
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Registration failed: {str(e)}"
        )


@router.post("/login", response_model=Dict[str, str])
async def login_user(
    user_login: UserLogin,
    session: AsyncSession = Depends(get_async_session)
):
    """Login a user and return access and refresh tokens."""
    auth_service = AuthService(session)

    user = await auth_service.authenticate_user(user_login.email, user_login.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Inactive user",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create access token
    access_token = await auth_service.create_access_token_for_user(user)

    # Capture user_id before it might be expired by commit in next step
    user_id = user.id

    # Create refresh token
    refresh_token_service = RefreshTokenService(session)
    refresh_token_record, plain_refresh_token = await refresh_token_service.create_refresh_token(user_id)
    
    # Create composite refresh token: user_id:token
    # This allows efficient lookup and verification without decoding a JWT
    composite_refresh_token = f"{user_id}:{plain_refresh_token}"

    return {
        "access_token": access_token,
        "refresh_token": composite_refresh_token,
        "token_type": "bearer"
    }


class RefreshTokenRequest(BaseModel):
    refresh_token: str


@router.post("/refresh", response_model=Dict[str, str])
async def refresh_access_token(
    request: RefreshTokenRequest,
    session: AsyncSession = Depends(get_async_session)
):
    """Refresh access token using refresh token."""
    refresh_token_service = RefreshTokenService(session)
    auth_service = AuthService(session)

    try:
        # Parse composite token
        if ":" not in request.refresh_token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token format",
                headers={"WWW-Authenticate": "Bearer"},
            )
            
        user_id_str, plain_token = request.refresh_token.split(":", 1)
        try:
            user_id = UUID(user_id_str)
        except ValueError:
             raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid user ID in token",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Verify token
        token_record = await refresh_token_service.verify_refresh_token(plain_token, user_id)
        if not token_record:
             raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired refresh token",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Get user
        user = await auth_service.get_user_by_id(user_id)
        if not user or not user.is_active:
             raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found or inactive",
                headers={"WWW-Authenticate": "Bearer"},
            )
            
        # Create new access token
        new_access_token = await auth_service.create_access_token_for_user(user)

        return {
            "access_token": new_access_token,
            "token_type": "bearer"
        }
        
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )


@router.post("/logout")
async def logout_user(
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session)
):
    """Logout user and revoke refresh tokens."""
    # Revoke all refresh tokens for the current user
    refresh_token_service = RefreshTokenService(session)
    revoked_count = await refresh_token_service.revoke_all_user_tokens(current_user.id)

    return {"message": f"Logged out successfully. Revoked {revoked_count} refresh tokens."}