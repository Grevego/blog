"""
Authentication and authorization dependencies.
"""

from typing import Optional
from uuid import UUID
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.services.auth_service import auth_service

# HTTP Bearer token scheme for JWT authentication
security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """
    Get current user from JWT token in Authorization header.
    
    Expects: Authorization: Bearer <jwt-token>
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        user = auth_service.get_current_user_from_token(db, credentials.credentials)
        if user is None:
            raise credentials_exception
        
        if not bool(user.is_active):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Inactive user"
            )
        
        return user
    except Exception:
        raise credentials_exception


def get_current_user_optional(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(
        HTTPBearer(auto_error=False)
    ),
    db: Session = Depends(get_db)
) -> Optional[User]:
    """
    Get current user optionally (for endpoints that work with or without auth).
    """
    if not credentials:
        return None
    
    try:
        return get_current_user(credentials, db)
    except HTTPException:
        return None


def get_current_superuser(
    current_user: User = Depends(get_current_user)
) -> User:
    """
    Require current user to be a superuser.
    """
    if not bool(current_user.is_superuser):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    return current_user


def verify_post_ownership(
    post_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> User:
    """
    Verify that the current user owns the specified post or is a superuser.
    """
    from app.services.post_service import post_service
    
    post = post_service.get(db, post_id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )
    
    if str(post.author_id) != str(current_user.id) and not bool(current_user.is_superuser):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions to access this post"
        )
    
    return current_user 