from datetime import date
from typing import List, Optional
from uuid import UUID
from pydantic import Field

from .base import BaseSchema, BaseResponseSchema, PaginatedResponse
from .user import UserResponse
from .category import CategoryResponse


class PostBase(BaseSchema):
    """Base post schema with common fields."""
    title: str = Field(..., min_length=1, max_length=255)
    slug: str = Field(..., min_length=1, max_length=255)
    excerpt: Optional[str] = None
    content: str = Field(..., min_length=1)
    image_url: Optional[str] = Field(None, max_length=512)
    meta_title: Optional[str] = Field(None, max_length=255)
    meta_description: Optional[str] = Field(None, max_length=500)


class PostCreate(PostBase):
    """Schema for creating a new post."""
    category_ids: List[UUID] = Field(default_factory=list)
    published_at: Optional[date] = None
    is_published: bool = False
    is_featured: bool = False
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "Getting Started with FastAPI",
                "slug": "getting-started-with-fastapi",
                "excerpt": "Learn how to build APIs with FastAPI",
                "content": "FastAPI is a modern web framework...",
                "image_url": "https://example.com/image.jpg",
                "category_ids": ["123e4567-e89b-12d3-a456-426614174000"],
                "is_published": True,
                "is_featured": False,
                "meta_title": "FastAPI Tutorial",
                "meta_description": "Complete guide to FastAPI"
            }
        }
    }


class PostUpdate(BaseSchema):
    """Schema for updating post information."""
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    slug: Optional[str] = Field(None, min_length=1, max_length=255)
    excerpt: Optional[str] = None
    content: Optional[str] = Field(None, min_length=1)
    image_url: Optional[str] = Field(None, max_length=512)
    category_ids: Optional[List[UUID]] = None
    published_at: Optional[date] = None
    is_published: Optional[bool] = None
    is_featured: Optional[bool] = None
    meta_title: Optional[str] = Field(None, max_length=255)
    meta_description: Optional[str] = Field(None, max_length=500)


class PostResponse(BaseResponseSchema, PostBase):
    """Schema for post response."""
    published_at: Optional[date] = None
    is_published: bool
    is_featured: bool
    author: UserResponse
    categories: List[CategoryResponse] = Field(default_factory=list)
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "title": "Getting Started with FastAPI",
                "slug": "getting-started-with-fastapi",
                "excerpt": "Learn how to build APIs with FastAPI",
                "content": "FastAPI is a modern web framework...",
                "image_url": "https://example.com/image.jpg",
                "published_at": "2024-01-01",
                "is_published": True,
                "is_featured": False,
                "meta_title": "FastAPI Tutorial",
                "meta_description": "Complete guide to FastAPI",
                "author": {
                    "id": "456e7890-e89b-12d3-a456-426614174000",
                    "username": "johndoe",
                    "full_name": "John Doe"
                },
                "categories": [
                    {
                        "id": "789e0123-e89b-12d3-a456-426614174000",
                        "name": "Technology",
                        "slug": "technology"
                    }
                ],
                "created_at": "2024-01-01T00:00:00Z",
                "updated_at": "2024-01-01T00:00:00Z"
            }
        }
    }


class PostListResponse(PaginatedResponse):
    """Schema for paginated post list response."""
    items: List[PostResponse] 