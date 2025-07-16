from typing import Optional, List
from uuid import UUID
from sqlalchemy.orm import Session, selectinload
from fastapi import HTTPException, status

from app.models.post import Post
from app.models.category import Category
from app.schemas.post import PostCreate, PostUpdate
from .base_service import BaseService


class PostService(BaseService[Post, PostCreate, PostUpdate]):
    """Service for post operations."""
    
    def __init__(self):
        super().__init__(Post)

    def get_by_slug(self, db: Session, slug: str) -> Optional[Post]:
        """Get post by slug with author and categories."""
        return (
            db.query(Post)
            .options(selectinload(Post.author), selectinload(Post.categories))
            .filter(Post.slug == slug)
            .first()
        )

    def get_published_posts(
        self, 
        db: Session, 
        skip: int = 0, 
        limit: int = 100
    ) -> List[Post]:
        """Get published posts with author and categories."""
        return (
            db.query(Post)
            .options(selectinload(Post.author), selectinload(Post.categories))
            .filter(Post.is_published == True)
            .order_by(Post.published_at.desc(), Post.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_featured_posts(self, db: Session, limit: int = 5) -> List[Post]:
        """Get featured published posts."""
        return (
            db.query(Post)
            .options(selectinload(Post.author), selectinload(Post.categories))
            .filter(Post.is_published == True, Post.is_featured == True)
            .order_by(Post.published_at.desc())
            .limit(limit)
            .all()
        )

    def get_posts_by_category(
        self, 
        db: Session, 
        category_slug: str, 
        skip: int = 0, 
        limit: int = 100
    ) -> List[Post]:
        """Get published posts by category slug."""
        return (
            db.query(Post)
            .options(selectinload(Post.author), selectinload(Post.categories))
            .join(Post.categories)
            .filter(Category.slug == category_slug, Post.is_published == True)
            .order_by(Post.published_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_posts_by_author(
        self, 
        db: Session, 
        author_id: UUID, 
        skip: int = 0, 
        limit: int = 100
    ) -> List[Post]:
        """Get posts by author (including unpublished for the author)."""
        return (
            db.query(Post)
            .options(selectinload(Post.author), selectinload(Post.categories))
            .filter(Post.author_id == author_id)
            .order_by(Post.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    def create_post(self, db: Session, post_in: PostCreate, author_id: UUID) -> Post:
        """Create a new post with author and categories."""
        # Check if slug already exists
        if self.get_by_slug(db, post_in.slug):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Post slug already exists"
            )

        # Get categories
        categories = []
        if post_in.category_ids:
            categories = db.query(Category).filter(
                Category.id.in_(post_in.category_ids)
            ).all()
            
            if len(categories) != len(post_in.category_ids):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="One or more categories not found"
                )

        # Create post data
        post_data = post_in.model_dump()
        del post_data['category_ids']
        post_data['author_id'] = author_id

        # Create post
        db_post = Post(**post_data)
        db_post.categories = categories
        
        db.add(db_post)
        db.commit()
        db.refresh(db_post)
        return db_post

    def update_post(
        self, 
        db: Session, 
        post_id: UUID, 
        post_in: PostUpdate
    ) -> Post:
        """Update post with categories."""
        post = self.get_or_404(db, post_id)
        
        # Check if new slug conflicts with existing posts
        if post_in.slug is not None and post_in.slug != str(post.slug):
            existing_post = self.get_by_slug(db, post_in.slug)
            if existing_post is not None:
                if str(existing_post.id) != str(post.id):
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Post slug already exists"
                    )

        # Handle category updates
        if post_in.category_ids is not None:
            categories = db.query(Category).filter(
                Category.id.in_(post_in.category_ids)
            ).all()
            
            if len(categories) != len(post_in.category_ids):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="One or more categories not found"
                )
            
            post.categories = categories

        # Update other fields
        update_data = post_in.model_dump(exclude_unset=True, exclude={'category_ids'})
        for field, value in update_data.items():
            if hasattr(post, field):
                setattr(post, field, value)

        db.add(post)
        db.commit()
        db.refresh(post)
        return post

    def search_posts(
        self, 
        db: Session, 
        query: str, 
        skip: int = 0, 
        limit: int = 100
    ) -> List[Post]:
        """Search posts by title and content."""
        return (
            db.query(Post)
            .options(selectinload(Post.author), selectinload(Post.categories))
            .filter(
                Post.is_published == True,
                (Post.title.ilike(f"%{query}%") | Post.content.ilike(f"%{query}%"))
            )
            .order_by(Post.published_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    def count_published_posts(self, db: Session) -> int:
        """Count published posts."""
        return db.query(Post).filter(Post.is_published == True).count()


# Global service instance
post_service = PostService() 