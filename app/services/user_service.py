from typing import Optional
from uuid import UUID
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
import bcrypt

from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from .base_service import BaseService


class UserService(BaseService[User, UserCreate, UserUpdate]):
    """Service for user operations with authentication support."""
    
    def __init__(self):
        super().__init__(User)

    def get_by_username(self, db: Session, username: str) -> Optional[User]:
        """Get user by username."""
        return db.query(User).filter(User.username == username).first()

    def get_by_email(self, db: Session, email: str) -> Optional[User]:
        """Get user by email."""
        return db.query(User).filter(User.email == email).first()

    def create_user(self, db: Session, user_in: UserCreate) -> User:
        """Create a new user with hashed password."""
        # Check if username already exists
        if self.get_by_username(db, user_in.username):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already registered"
            )
        
        # Check if email already exists
        if self.get_by_email(db, user_in.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )

        # Hash password
        hashed_password = self._hash_password(user_in.password)
        
        # Create user data without password
        user_data = user_in.model_dump()
        del user_data['password']
        user_data['hashed_password'] = hashed_password

        # Create user
        db_user = User(**user_data)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    def authenticate(self, db: Session, username: str, password: str) -> Optional[User]:
        """Authenticate user with username and password."""
        user = self.get_by_username(db, username)
        if not user:
            return None
        
        # Convert SQLAlchemy Column to string for type safety
        if not self._verify_password(password, str(user.hashed_password)):
            return None
        
        return user

    def is_active(self, user: User) -> bool:
        """Check if user is active."""
        return bool(user.is_active)

    def is_superuser(self, user: User) -> bool:
        """Check if user is superuser."""
        return bool(user.is_superuser)

    def get_posts_count(self, db: Session, user_id: UUID) -> int:
        """Get the number of posts by a user."""
        user = db.query(User).filter(User.id == user_id).first()
        if user:
            return user.posts.count()
        return 0

    def _hash_password(self, password: str) -> str:
        """Hash a password using bcrypt."""
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

    def _verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify a password against its hash."""
        return bcrypt.checkpw(
            plain_password.encode('utf-8'), 
            hashed_password.encode('utf-8')
        )


# Global service instance
user_service = UserService() 