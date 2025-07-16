from typing import Optional
from pydantic import Field

from .base import BaseSchema, BaseResponseSchema


class CategoryBase(BaseSchema):
    """Base category schema with common fields."""
    name: str = Field(..., min_length=1, max_length=100)
    slug: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    color: Optional[str] = Field(None, pattern=r'^#[0-9A-Fa-f]{6}$')


class CategoryCreate(CategoryBase):
    """Schema for creating a new category."""
    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "Technology",
                "slug": "technology",
                "description": "All about tech trends and innovations",
                "color": "#3B82F6"
            }
        }
    }


class CategoryUpdate(BaseSchema):
    """Schema for updating category information."""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    slug: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = None
    color: Optional[str] = Field(None, pattern=r'^#[0-9A-Fa-f]{6}$')


class CategoryResponse(BaseResponseSchema, CategoryBase):
    """Schema for category response."""
    posts_count: Optional[int] = 0
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "name": "Technology",
                "slug": "technology", 
                "description": "All about tech trends and innovations",
                "color": "#3B82F6",
                "posts_count": 5,
                "created_at": "2024-01-01T00:00:00Z",
                "updated_at": "2024-01-01T00:00:00Z"
            }
        }
    } 