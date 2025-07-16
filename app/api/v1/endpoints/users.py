from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.user import UserCreate, UserUpdate, UserResponse
from app.services.user_service import user_service

router = APIRouter()


@router.get("/", response_model=List[UserResponse])
def get_users(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=50),
    active_only: bool = Query(True, description="Show only active users"),
    # TODO: Add authentication - only admins should list all users
    # current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """
    Get all users.
    
    **Note**: This endpoint will require admin authentication in production.
    
    - **page**: Page number
    - **size**: Users per page
    - **active_only**: Filter to show only active users
    """
    skip = (page - 1) * size
    users = user_service.get_multi(db, skip, size)
    
    if active_only:
        users = [user for user in users if user_service.is_active(user)]
    
    return users


@router.get("/me", response_model=UserResponse)
def get_current_user(
    # TODO: Add authentication
    # current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get current user profile.
    
    **Note**: This endpoint requires authentication.
    Currently returns a placeholder response.
    """
    # TODO: Return actual current user
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Authentication not implemented yet"
    )


@router.get("/{user_id}", response_model=UserResponse)
def get_user_by_id(
    user_id: UUID,
    db: Session = Depends(get_db)
):
    """Get user profile by ID (public information only)."""
    user = user_service.get_or_404(db, user_id)
    
    if not user_service.is_active(user):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return user


@router.get("/username/{username}", response_model=UserResponse)
def get_user_by_username(
    username: str,
    db: Session = Depends(get_db)
):
    """Get user profile by username (public information only)."""
    user = user_service.get_by_username(db, username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    if not user_service.is_active(user):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return user


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register_user(
    user_in: UserCreate,
    db: Session = Depends(get_db)
):
    """
    Register a new user account.
    
    - **username**: Unique username (3-50 characters)
    - **email**: Valid email address
    - **full_name**: User's full name
    - **password**: Password (minimum 8 characters)
    - **bio**: Optional user bio
    - **website_url**: Optional website URL
    """
    return user_service.create_user(db, user_in)


@router.put("/me", response_model=UserResponse)
def update_current_user(
    user_in: UserUpdate,
    # TODO: Add authentication
    # current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update current user profile.
    
    **Note**: This endpoint requires authentication.
    """
    # TODO: Implement with actual current user
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Authentication not implemented yet"
    )


@router.put("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: UUID,
    user_in: UserUpdate,
    # TODO: Add authentication and authorization
    # current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """
    Update user profile (admin only).
    
    **Note**: This endpoint will require admin authentication in production.
    """
    user = user_service.get_or_404(db, user_id)
    return user_service.update(db, user, user_in)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: UUID,
    # TODO: Add authentication and authorization
    # current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """
    Delete user account (admin only).
    
    **Note**: This endpoint will require admin authentication in production.
    **Warning**: This will also delete all posts by this user.
    """
    user = user_service.get_or_404(db, user_id)
    user_service.remove(db, user_id)


@router.get("/{user_id}/posts")
def get_user_posts(
    user_id: UUID,
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=50),
    published_only: bool = Query(True, description="Show only published posts"),
    db: Session = Depends(get_db)
):
    """Get posts by a specific user."""
    # Verify user exists
    user = user_service.get_or_404(db, user_id)
    
    # Import here to avoid circular imports
    from app.services.post_service import post_service
    
    skip = (page - 1) * size
    posts = post_service.get_posts_by_author(db, user_id, skip, size)
    
    # Filter published posts for public access
    # TODO: If current_user == user or current_user is admin, show all posts
    if published_only:
        posts = [post for post in posts if bool(post.is_published)]
    
    return {
        "user": user,
        "posts": posts,
        "page": page,
        "size": size,
        "total_posts": user_service.get_posts_count(db, user_id)
    }


@router.post("/login")
def login_user(
    # TODO: Implement login with username/password
    db: Session = Depends(get_db)
):
    """
    User login endpoint.
    
    **Note**: Authentication system not implemented yet.
    This will return JWT tokens in production.
    """
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Authentication not implemented yet"
    ) 