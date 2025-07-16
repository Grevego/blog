from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, ConfigDict


class BaseSchema(BaseModel):
    """Base schema with common configuration."""
    model_config = ConfigDict(from_attributes=True)


class BaseResponseSchema(BaseSchema):
    """Base response schema with common fields."""
    id: UUID
    created_at: datetime
    updated_at: datetime


class PaginationParams(BaseModel):
    """Pagination parameters for list endpoints."""
    page: int = 1
    size: int = 10
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "page": 1,
                "size": 10
            }
        }
    )


class PaginatedResponse(BaseModel):
    """Generic paginated response."""
    items: list
    total: int
    page: int
    size: int
    pages: int 