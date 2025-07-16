"""
Authentication and authorization dependencies.
"""

from typing import Optional
from uuid import UUID
from fastapi import Depends, HTTPException, status, Query, Header
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.services.user_service import user_service


def get_current_user_by_id(
    user_id: UUID = Query(..., description="User ID for authentication (testing only)"),
    db: Session = Depends(get_db)
) -> User:
    """
    Get current user by user_id query parameter.
    
    This is a simple authentication method for testing purposes.
    In production, you would validate JWT tokens or session cookies.
    """
    user = user_service.get(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    if not bool(user.is_active):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    
    return user


def get_current_user_optional(
    user_id: Optional[UUID] = Query(None, description="Optional user ID for authentication"),
    db: Session = Depends(get_db)
) -> Optional[User]:
    """
    Get current user optionally (for endpoints that work with or without auth).
    """
    if not user_id:
        return None
    
    try:
        return get_current_user_by_id(user_id, db)
    except HTTPException:
        return None


def get_current_superuser(
    current_user: User = Depends(get_current_user_by_id)
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
    current_user: User = Depends(get_current_user_by_id),
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