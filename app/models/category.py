from sqlalchemy import Column, String, Text
from sqlalchemy.orm import relationship

from .base import BaseModel


class Category(BaseModel):
    """Category model for organizing blog posts."""
    __tablename__ = 'categories'

    # Category information
    name = Column(String(100), nullable=False, unique=True, index=True)
    slug = Column(String(100), nullable=False, unique=True, index=True)
    description = Column(Text)
    color = Column(String(7))  # Hex color code like #FF5733
    
    # Relationships
    posts = relationship(
        'Post',
        secondary='post_categories',
        back_populates='categories',
        lazy="dynamic"
    )

    def __repr__(self):
        return f"<Category(name={self.name}, slug={self.slug})>" 