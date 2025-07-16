from typing import Optional
from pydantic import EmailStr, Field

from .base import BaseSchema, BaseResponseSchema


class UserBase(BaseSchema):
    """Base user schema with common fields."""
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    full_name: str = Field(..., min_length=1, max_length=255)
    bio: Optional[str] = Field(None, max_length=500)
    avatar_url: Optional[str] = Field(None, max_length=512)
    website_url: Optional[str] = Field(None, max_length=512)


class UserCreate(UserBase):
    """Schema for creating a new user."""
    password: str = Field(..., min_length=8, max_length=100)
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "username": "johndoe",
                "email": "john@example.com",
                "full_name": "John Doe",
                "password": "securepassword123",
                "bio": "A passionate blogger",
                "website_url": "https://johndoe.com"
            }
        }
    }


class UserUpdate(BaseSchema):
    """Schema for updating user information."""
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    email: Optional[EmailStr] = None
    full_name: Optional[str] = Field(None, min_length=1, max_length=255)
    bio: Optional[str] = Field(None, max_length=500)
    avatar_url: Optional[str] = Field(None, max_length=512)
    website_url: Optional[str] = Field(None, max_length=512)
    is_active: Optional[bool] = None


class UserResponse(BaseResponseSchema, UserBase):
    """Schema for user response."""
    is_active: bool
    is_superuser: bool
    
    # Exclude sensitive fields
    model_config = {
        "json_schema_extra": {
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "username": "johndoe",
                "email": "john@example.com",
                "full_name": "John Doe",
                "bio": "A passionate blogger",
                "avatar_url": "https://example.com/avatar.jpg",
                "website_url": "https://johndoe.com",
                "is_active": True,
                "is_superuser": False,
                "created_at": "2024-01-01T00:00:00Z",
                "updated_at": "2024-01-01T00:00:00Z"
            }
        }
    } 