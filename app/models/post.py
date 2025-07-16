from sqlalchemy import Column, String, Text, Date, Boolean, Table, ForeignKey
from sqlalchemy.orm import relationship

from .base import BaseModel, GUID


# Association table for posts ↔ categories (many-to-many)
post_categories = Table(
    'post_categories',
    BaseModel.metadata,
    Column('post_id', GUID(), ForeignKey('posts.id', ondelete='CASCADE'), primary_key=True),
    Column('category_id', GUID(), ForeignKey('categories.id', ondelete='CASCADE'), primary_key=True)
)


class Post(BaseModel):
    """Blog post model."""
    __tablename__ = 'posts'

    # Post content
    title = Column(String(255), nullable=False, index=True)
    slug = Column(String(255), nullable=False, unique=True, index=True)
    excerpt = Column(Text)
    content = Column(Text, nullable=False)
    
    # Media and publishing
    image_url = Column(String(512))
    published_at = Column(Date)
    is_published = Column(Boolean, default=False, nullable=False)
    is_featured = Column(Boolean, default=False, nullable=False)
    
    # SEO
    meta_title = Column(String(255))
    meta_description = Column(String(500))
    
    # Author relationship
    author_id = Column(GUID(), ForeignKey('users.id'), nullable=False)
    author = relationship("User", back_populates="posts")
    
    # Category relationships (many-to-many)
    categories = relationship(
        'Category',
        secondary=post_categories,
        back_populates='posts',
        lazy="selectin"
    )

    def __repr__(self):
        return f"<Post(title={self.title}, slug={self.slug}, published={self.is_published})>" 