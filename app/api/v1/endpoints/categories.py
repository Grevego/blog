from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.category import CategoryCreate, CategoryUpdate, CategoryResponse
from app.services.category_service import category_service

router = APIRouter()


@router.get("/", response_model=List[CategoryResponse])
def get_categories(
    with_post_count: bool = Query(False, description="Include post count for each category"),
    popular: bool = Query(False, description="Get categories ordered by post count"),
    limit: int = Query(None, ge=1, le=100, description="Limit number of categories"),
    db: Session = Depends(get_db)
):
    """
    Get all categories.
    
    - **with_post_count**: Include the number of posts in each category
    - **popular**: Order categories by post count (most popular first)
    - **limit**: Maximum number of categories to return
    """
    if popular:
        categories = category_service.get_popular_categories(db, limit or 10)
    elif with_post_count:
        categories = category_service.get_categories_with_post_count(db)
    else:
        categories = category_service.get_multi(db, limit=limit or 100)
    
    return categories


@router.get("/{slug}", response_model=CategoryResponse)
def get_category_by_slug(
    slug: str,
    db: Session = Depends(get_db)
):
    """
    Get a category by its slug.
    
    - **slug**: The URL-friendly category identifier
    """
    category = category_service.get_by_slug(db, slug)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )
    return category


@router.get("/{category_id}/posts")
def get_category_posts(
    category_id: UUID,
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db)
):
    """Get all published posts in a specific category."""
    # First verify category exists
    category = category_service.get_or_404(db, category_id)
    
    # Import here to avoid circular imports
    from app.services.post_service import post_service
    
    skip = (page - 1) * size
    posts = post_service.get_posts_by_category(db, str(category.slug), skip, size)
    
    return {
        "category": category,
        "posts": posts,
        "page": page,
        "size": size
    }


@router.post("/", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
def create_category(
    category_in: CategoryCreate,
    # TODO: Add authentication - only admins should create categories
    # current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """
    Create a new category.
    
    **Note**: This endpoint will require admin authentication in production.
    
    - **name**: Display name of the category
    - **slug**: URL-friendly identifier (must be unique)
    - **description**: Optional description of the category
    - **color**: Optional hex color code for UI theming
    """
    return category_service.create_category(db, category_in)


@router.put("/{category_id}", response_model=CategoryResponse)
def update_category(
    category_id: UUID,
    category_in: CategoryUpdate,
    # TODO: Add authentication - only admins should update categories
    # current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """
    Update an existing category.
    
    **Note**: This endpoint will require admin authentication in production.
    """
    return category_service.update_category(db, category_id, category_in)


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(
    category_id: UUID,
    # TODO: Add authentication - only admins should delete categories
    # current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """
    Delete a category.
    
    **Note**: This endpoint will require admin authentication in production.
    **Warning**: This will remove the category from all posts that use it.
    """
    category = category_service.get_or_404(db, category_id)
    category_service.remove(db, category_id)


@router.get("/popular/top", response_model=List[CategoryResponse])
def get_top_categories(
    limit: int = Query(5, ge=1, le=20, description="Number of top categories"),
    db: Session = Depends(get_db)
):
    """Get the most popular categories by post count."""
    return category_service.get_popular_categories(db, limit) 