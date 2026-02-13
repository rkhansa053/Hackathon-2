import logging
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
from .config.settings import settings
from .api.v1 import tasks, auth
from contextlib import asynccontextmanager
from .config.database import init_db
import time


# Configure structured logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize the database on startup
    await init_db()
    logger.info("Database initialized")
    yield
    # Cleanup on shutdown if needed
    logger.info("Shutting down")


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    debug=settings.debug,
    lifespan=lifespan
)


# Custom exception handler for validation errors
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle request validation errors with proper error responses."""
    logger.warning(f"Validation error: {exc.errors()}")

    errors = []
    for error in exc.errors():
        errors.append({
            "loc": error["loc"],
            "msg": error["msg"],
            "type": error["type"]
        })

    return JSONResponse(
        status_code=422,
        content={
            "detail": errors,
            "message": "Request validation failed"
        }
    )


# Global exception handler for all other exceptions
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Handle all other exceptions."""
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)

    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error",
            "message": "An unexpected error occurred"
        }
    )


# Middleware for logging requests
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()

    response = await call_next(request)

    process_time = time.time() - start_time
    logger.info(
        f"{request.method} {request.url.path} "
        f"{response.status_code} {process_time:.2f}s"
    )

    return response


# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Security headers middleware
class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response: Response = await call_next(request)

        # Add security headers to all responses
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"

        return response


# Add security headers middleware
app.add_middleware(SecurityHeadersMiddleware)


# Add trusted host middleware for security
# Note: TrustedHostMiddleware expects hostnames only, not full URLs
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=settings.allowed_hosts
)


@app.get("/health")
async def health_check():
    """Health check endpoint to verify the application is running."""
    logger.info("Health check endpoint called")
    return {"status": "healthy", "timestamp": "2026-01-30T10:00:00Z"}


# Include API routes
app.include_router(tasks.router, prefix="/api/v1", tags=["tasks"])
app.include_router(auth.router, prefix="/api/v1", tags=["auth"])


if __name__ == "__main__":
    import uvicorn
    import os
    
    # Hugging Face Spaces uses port 7860 by default
    # Render and other platforms use the PORT env var
    port = int(os.getenv("PORT", 7860))
    host = os.getenv("HOST", "0.0.0.0")
    
    logger.info(f"Starting server on {host}:{port}")
    
    uvicorn.run(
        "src.main:app",
        host=host,
        port=port,
        reload=settings.debug  # Only reload if debug mode is explicitly enabled
    )