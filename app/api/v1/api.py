from fastapi import APIRouter

from app.api.v1.endpoints import auth, posts, categories, users

# Create main API router for v1
api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(
    auth.router, 
    prefix="/auth", 
    tags=["authentication"]
)

api_router.include_router(
    posts.router, 
    prefix="/posts", 
    tags=["posts"]
)

api_router.include_router(
    categories.router, 
    prefix="/categories", 
    tags=["categories"]
)

api_router.include_router(
    users.router, 
    prefix="/users", 
    tags=["users"]
)

# Health check endpoint
@api_router.get("/health")
def health_check():
    """Health check endpoint to verify API is running."""
    return {
        "status": "healthy",
        "message": "FastAPI Blog API is running",
        "version": "1.0.0"
    }

# Root endpoint
@api_router.get("/")
def api_info():
    """API information endpoint."""
    return {
        "name": "FastAPI Blog API",
        "version": "1.0.0",
        "description": "A modern blog API built with FastAPI",
        "endpoints": {
            "auth": "/api/v1/auth",
            "posts": "/api/v1/posts",
            "categories": "/api/v1/categories", 
            "users": "/api/v1/users",
            "health": "/api/v1/health"
        },
        "docs": "/docs",
        "redoc": "/redoc"
    } 