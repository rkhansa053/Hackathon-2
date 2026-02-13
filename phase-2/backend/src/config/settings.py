from pydantic_settings import BaseSettings
from pydantic import ConfigDict, field_validator
from typing import Any


class Settings(BaseSettings):
    # Application settings
    app_name: str = "Todo Backend API"
    app_version: str = "0.1.0"
    debug: bool = False

    # Database settings
    database_url: str = "sqlite+aiosqlite:///./todo_test.db"

    # Security settings
    secret_key: str = "your-secret-key-here-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    better_auth_secret: str = "your-super-secret-key-here-change-in-production"

    # CORS
    allowed_origins: list[str] = []

    # Trusted Hosts
    allowed_hosts: list[str] = ["localhost", "127.0.0.1", "*.vercel.app", "*.hf.space", "*.ngrok.io"]

    @field_validator("allowed_origins", "allowed_hosts", mode="before")
    @classmethod
    def parse_comma_separated_list(cls, v: Any):
        if not v:
            return []
        if isinstance(v, str):
            # Handle JSON-style list strings like ["a", "b"]
            if v.startswith("[") and v.endswith("]"):
                import json
                try:
                    return json.loads(v)
                except json.JSONDecodeError:
                    v = v[1:-1] # Fallback to stripping brackets
            return [i.strip().strip('"').strip("'") for i in v.split(",") if i.strip()]
        return v

    model_config = ConfigDict(
        env_file=".env",
        env_parse_none_str=None,
        extra="ignore",
    )


settings = Settings()
