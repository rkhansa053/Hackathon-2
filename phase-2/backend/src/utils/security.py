from datetime import datetime, timedelta
from typing import Optional
import uuid
from passlib.context import CryptContext
from jose import JWTError, jwt
from ..config.settings import settings


# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against a hashed password."""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Hash a plain password."""
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create a JWT access token."""
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    return encoded_jwt


def create_refresh_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create a JWT refresh token with longer expiration."""
    to_encode = data.copy()

    # Default to 7 days if no expiration is provided
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(days=7)

    to_encode.update({"exp": expire, "type": "refresh"})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    return encoded_jwt


def verify_token(token: str, token_type: str = "access") -> Optional[dict]:
    """Verify a JWT token and return the payload if valid."""
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])

        # Check if token type matches (for refresh tokens)
        if token_type == "refresh":
            token_type_claim = payload.get("type")
            if token_type_claim != "refresh":
                return None

        return payload
    except JWTError:
        return None


def decode_token_payload(token: str) -> Optional[dict]:
    """Decode JWT token without verification (for inspection only)."""
    try:
        # This decodes without verification - use carefully
        payload = jwt.get_unverified_claims(token)
        return payload
    except JWTError:
        return None


def get_user_id_from_token(token: str) -> Optional[uuid.UUID]:
    """Extract user ID from a JWT token."""
    payload = verify_token(token)
    if payload:
        user_id_str = payload.get("sub")  # Using "sub" as standard JWT claim for user ID
        if user_id_str:
            try:
                return uuid.UUID(user_id_str)
            except ValueError:
                return None
    return None


def is_token_expired(token: str) -> bool:
    """Check if a token is expired."""
    payload = decode_token_payload(token)
    if payload:
        exp = payload.get("exp")
        if exp:
            return datetime.fromtimestamp(exp) < datetime.utcnow()
    return True