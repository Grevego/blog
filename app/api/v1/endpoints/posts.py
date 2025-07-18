from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user, verify_post_ownership
from app.models.user import User
from app.schemas.post import PostCreate, PostUpdate, PostResponse, PostListResponse
from app.schemas.base import PaginationParams, PaginatedResponse
from app.services.post_service import post_service

router = APIRouter()


@router.get("/", response_model=PostListResponse)
def get_posts(
    page: int = Query(1, ge=1, description="Page number"),
    size: int = Query(10, ge=1, le=100, description="Items per page"),
    category: Optional[str] = Query(None, description="Filter by category slug"),
    search: Optional[str] = Query(None, description="Search in title and content"),
    featured: Optional[bool] = Query(None, description="Filter featured posts"),
    db: Session = Depends(get_db)
):
    """
    Get published posts with optional filtering.
    
    - **page**: Page number (starts from 1)
    - **size**: Number of posts per page (max 100)
    - **category**: Filter posts by category slug
    - **search**: Search term for title and content
    - **featured**: Filter only featured posts
    """
    skip = (page - 1) * size
    
    # Handle different filtering scenarios
    if search:
        if len(search.strip()) < 2:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Search query must be at least 2 characters long"
            )
        posts = post_service.search_posts(db, search, skip, size)
        total = len(posts)  # For simplicity, not implementing count for search
        if not posts:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No posts found matching '{search}'"
            )
    elif category:
        # Verify category exists first
        from app.services.category_service import category_service
        if not category_service.get_by_slug(db, category):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Category '{category}' not found"
            )
        posts = post_service.get_posts_by_category(db, category, skip, size)
        total = len(posts)  # For simplicity
        if not posts:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No published posts found in category '{category}'"
            )
    elif featured:
        posts = post_service.get_featured_posts(db, size)
        total = len(posts)
        if not posts:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No featured posts available at this time"
            )
    else:
        posts = post_service.get_published_posts(db, skip, size)
        total = post_service.count_published_posts(db)
        if not posts and page == 1:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No published posts available. Check back later for new content!"
            )
        elif not posts and page > 1:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Page {page} does not exist. Total posts: {total}"
            )
    
    pages = (total + size - 1) // size  # Ceiling division
    
    return PostListResponse(
        items=[PostResponse.model_validate(post) for post in posts],
        total=total,
        page=page,
        size=size,
        pages=pages
    )


@router.get("/featured", response_model=List[PostResponse])
def get_featured_posts(
    limit: int = Query(5, ge=1, le=20, description="Number of featured posts"),
    db: Session = Depends(get_db)
):
    """Get featured posts for homepage or special sections."""
    return post_service.get_featured_posts(db, limit)


@router.get("/search", response_model=List[PostResponse])
def search_posts(
    q: str = Query(..., min_length=1, description="Search query"),
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db)
):
    """Search posts by title and content."""
    skip = (page - 1) * size
    return post_service.search_posts(db, q, skip, size)


@router.get("/{slug}", response_model=PostResponse)
def get_post_by_slug(
    slug: str,
    db: Session = Depends(get_db)
):
    """
    Get a single post by its slug.
    
    - **slug**: The URL-friendly post identifier
    """
    post = post_service.get_by_slug(db, slug)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )
    
    # Only show published posts to public
    if not bool(post.is_published):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )
    
    return post


@router.post("/", response_model=PostResponse, status_code=status.HTTP_201_CREATED)
def create_post(
    post_in: PostCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Create a new blog post.
    
    Requires JWT authentication via Authorization header.
    
    Example: 
    Authorization: Bearer <your-jwt-token>
    POST /api/v1/posts/
    """
    return post_service.create_post(db, post_in, UUID(str(current_user.id)))


@router.put("/{post_id}", response_model=PostResponse)
def update_post(
    post_id: UUID,
    post_in: PostUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(verify_post_ownership)
):
    """
    Update an existing post.
    
    Requires authentication and ownership verification.
    Only the post author or superuser can update a post.
    
    Example: PUT /api/v1/posts/{post_id}?user_id=your-user-uuid-here
    """
    return post_service.update_post(db, post_id, post_in)


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    post_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(verify_post_ownership)
):
    """
    Delete a post.
    
    Requires authentication and ownership verification.
    Only the post author or superuser can delete a post.
    
    Example: DELETE /api/v1/posts/{post_id}?user_id=your-user-uuid-here
    """
    post_service.remove(db, post_id)


@router.get("/author/{author_id}", response_model=List[PostResponse])
def get_posts_by_author(
    author_id: UUID,
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=50),
    # TODO: Add optional authentication to show unpublished posts to author
    db: Session = Depends(get_db)
):
    """Get posts by a specific author. Only shows published posts to public."""
    skip = (page - 1) * size
    posts = post_service.get_posts_by_author(db, author_id, skip, size)
    
    # Filter to only published posts for public access
    # TODO: If current_user == author, show all posts
    published_posts = [post for post in posts if bool(post.is_published)]
    
    return published_posts 