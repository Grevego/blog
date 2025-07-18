"""
Application configuration using environment variables.
"""

import os
from pydantic_settings import BaseSettings
from pydantic import Field
from typing import Optional


class Settings(BaseSettings):
    # Application settings
    app_name: str = "Blog API"
    environment: str = "development"
    debug: bool = True
    api_v1_prefix: str = "/api/v1"
    
    # Database settings
    database_url: Optional[str] = None
    
    # PostgreSQL settings for production
    postgres_user: str = "postgres"
    postgres_password: str = "password"
    postgres_host: str = "localhost"
    postgres_port: int = 5432
    postgres_db: str = "blog"
    
    # JWT Authentication settings
    secret_key: str = "your-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    @property
    def db_url(self) -> str:
        """Get database URL based on environment."""
        if self.database_url:
            return self.database_url
            
        if self.environment == "production":
            return f"postgresql://{self.postgres_user}:{self.postgres_password}@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        else:
            return "sqlite:///./blog.db"

    class Config:
        env_file = ".env"


settings = Settings() 