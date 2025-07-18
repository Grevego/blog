"""
Authentication schemas for login and token management.
"""

from pydantic import BaseModel


class UserLogin(BaseModel):
    """Schema for user login."""
    username: str
    password: str
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "username": "johndoe",
                "password": "secretpassword123"
            }
        }
    }


class Token(BaseModel):
    """Schema for JWT token response."""
    access_token: str
    token_type: str = "bearer"
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer"
            }
        }
    }


class TokenData(BaseModel):
    """Schema for token payload data."""
    username: str
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "username": "johndoe"
            }
        }
    } 