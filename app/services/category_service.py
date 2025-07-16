from typing import Optional, List
from uuid import UUID
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.category import Category
from app.schemas.category import CategoryCreate, CategoryUpdate
from .base_service import BaseService


class CategoryService(BaseService[Category, CategoryCreate, CategoryUpdate]):
    """Service for category operations."""
    
    def __init__(self):
        super().__init__(Category)

    def get_by_slug(self, db: Session, slug: str) -> Optional[Category]:
        """Get category by slug."""
        return db.query(Category).filter(Category.slug == slug).first()

    def get_by_name(self, db: Session, name: str) -> Optional[Category]:
        """Get category by name."""
        return db.query(Category).filter(Category.name == name).first()

    def create_category(self, db: Session, category_in: CategoryCreate) -> Category:
        """Create a new category with validation."""
        # Check if slug already exists
        if self.get_by_slug(db, category_in.slug):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Category slug already exists"
            )
        
        # Check if name already exists
        if self.get_by_name(db, category_in.name):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Category name already exists"
            )

        return self.create(db, category_in)

    def update_category(
        self, 
        db: Session, 
        category_id: UUID, 
        category_in: CategoryUpdate
    ) -> Category:
        """Update category with validation."""
        category = self.get_or_404(db, category_id)
        
        # Check if new slug conflicts with existing categories
        if category_in.slug is not None and category_in.slug != str(category.slug):
            existing_category = self.get_by_slug(db, category_in.slug)
            if existing_category is not None:
                if str(existing_category.id) != str(category.id):
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Category slug already exists"
                    )
        
        # Check if new name conflicts with existing categories
        if category_in.name is not None and category_in.name != str(category.name):
            existing_category = self.get_by_name(db, category_in.name)
            if existing_category is not None:
                if str(existing_category.id) != str(category.id):
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Category name already exists"
                    )

        return self.update(db, category, category_in)

    def get_categories_with_post_count(self, db: Session) -> List[Category]:
        """Get all categories with post count."""
        # This would require a more complex query in production
        # For now, we'll use the basic get_multi and add post count manually
        categories = self.get_multi(db)
        for category in categories:
            # Using the relationship to get count
            category.posts_count = category.posts.count()
        return categories

    def get_popular_categories(self, db: Session, limit: int = 10) -> List[Category]:
        """Get categories ordered by post count."""
        from sqlalchemy import func
        from app.models.post import post_categories
        
        return (
            db.query(Category)
            .join(post_categories)
            .group_by(Category.id)
            .order_by(func.count(post_categories.c.post_id).desc())
            .limit(limit)
            .all()
        )


# Global service instance
category_service = CategoryService() 