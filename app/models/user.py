from sqlalchemy import Column, String, Boolean
from sqlalchemy.orm import relationship

from .base import BaseModel


class User(BaseModel):
    """User model for blog post creators."""
    __tablename__ = 'users'

    # User information
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    full_name = Column(String(255), nullable=False)
    
    # Authentication (for future use)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    is_superuser = Column(Boolean, default=False, nullable=False)
    
    # Bio and profile
    bio = Column(String(500))
    avatar_url = Column(String(512))
    website_url = Column(String(512))
    
    # Relationships
    posts = relationship("Post", back_populates="author", lazy="dynamic")

    def __repr__(self):
        return f"<User(username={self.username}, email={self.email})>" 