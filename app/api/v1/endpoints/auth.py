"""
Authentication endpoints for login and token management.
"""

from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.schemas.auth import Token, UserLogin
from app.schemas.user import UserResponse
from app.services.auth_service import auth_service
from app.config import settings

router = APIRouter()


@router.post("/login", response_model=Token)
def login(
    user_credentials: UserLogin,
    db: Session = Depends(get_db)
):
    """
    Login endpoint for users to get JWT access token.
    
    - **username**: Your username or email
    - **password**: Your password
    
    Returns a JWT token that should be included in the Authorization header
    for authenticated requests: `Authorization: Bearer <token>`
    """
    user = auth_service.authenticate_user(
        db, user_credentials.username, user_credentials.password
    )
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not bool(user.is_active):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = auth_service.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    
    return Token(access_token=access_token, token_type="bearer")


@router.post("/login/form", response_model=Token)
def login_form(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """
    OAuth2 compatible login endpoint for Swagger UI.
    
    This endpoint accepts form data (username/password) and is compatible
    with FastAPI's automatic OAuth2 integration in the docs.
    """
    user = auth_service.authenticate_user(db, form_data.username, form_data.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not bool(user.is_active):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = auth_service.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    
    return Token(access_token=access_token, token_type="bearer")


@router.get("/me", response_model=UserResponse)
def get_current_user_info(
    current_user: User = Depends(get_current_user)
):
    """
    Get current user information from JWT token.
    
    This endpoint requires authentication. Include your JWT token in the
    Authorization header: `Authorization: Bearer <your-token>`
    """
    return current_user


@router.post("/logout")
def logout():
    """
    Logout endpoint.
    
    Since JWT tokens are stateless, logout is handled client-side by
    simply discarding the token. This endpoint is provided for completeness
    and could be extended to implement token blacklisting if needed.
    """
    return {"message": "Successfully logged out"} 