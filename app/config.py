from pydantic_settings import BaseSettings
from pydantic import Field, computed_field
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Environment configuration
    environment: str = Field(default="development", description="Environment (development, production)")
    
    # Database configuration
    database_url: Optional[str] = Field(default=None, description="Database URL")
    
    # PostgreSQL settings for production
    postgres_user: str = Field(default="postgres", description="PostgreSQL username")
    postgres_password: str = Field(default="password", description="PostgreSQL password")
    postgres_host: str = Field(default="localhost", description="PostgreSQL host")
    postgres_port: int = Field(default=5432, description="PostgreSQL port")
    postgres_db: str = Field(default="blog", description="PostgreSQL database name")
    
    @computed_field
    @property
    def db_url(self) -> str:
        """Get the appropriate database URL based on environment."""
        if self.database_url:
            # If DATABASE_URL is explicitly set, use it
            return self.database_url
        
        if self.environment.lower() == "production":
            # Use PostgreSQL for production
            return f"postgresql://{self.postgres_user}:{self.postgres_password}@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        else:
            # Use SQLite for development/testing
            return "sqlite:///./blog.db"
    
    # FastAPI configuration
    app_name: str = Field(default="FastAPI Blog", description="Application name")
    debug: bool = Field(default=True, description="Debug mode")
    
    # API configuration
    api_v1_prefix: str = Field(default="/api/v1", description="API v1 prefix")
    
    # Security (for future use)
    secret_key: Optional[str] = Field(default=None, description="Secret key for JWT")
    access_token_expire_minutes: int = Field(default=30, description="Token expiration time")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


# Global settings instance
settings = Settings() 