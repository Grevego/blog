from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.api.v1.api import api_router
from app.database import create_tables

# Create FastAPI application
app = FastAPI(
    title=settings.app_name,
    description="A modern blog API built with FastAPI, SQLAlchemy, and Alembic",
    version="1.0.0",
    debug=settings.debug,
)

# CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API router
app.include_router(api_router, prefix=settings.api_v1_prefix)

# Root endpoint
@app.get("/")
def root():
    """Root endpoint with basic API information."""
    return {
        "message": f"Welcome to {settings.app_name}",
        "docs": "/docs",
        "redoc": "/redoc",
        "api": settings.api_v1_prefix,
        "version": "1.0.0"
    }

# Health check endpoint
@app.get("/health")
def health():
    """Application health check."""
    return {
        "status": "healthy",
        "app": settings.app_name,
        "environment": settings.environment,
        "database": "connected"  # TODO: Add actual DB health check
    }

# Startup event
@app.on_event("startup")
def startup_event():
    """Initialize application on startup."""
    print(f"🚀 Starting {settings.app_name}")
    print(f"📊 Environment: {settings.environment}")
    print(f"🗄️  Database: {settings.db_url[:20]}...")
    print(f"🔧 Debug mode: {settings.debug}")
    
    # Create database tables
    create_tables()
    print("📋 Database tables created/verified")

# Shutdown event
@app.on_event("shutdown")
def shutdown_event():
    """Cleanup on application shutdown."""
    print(f"🛑 Shutting down {settings.app_name}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug
    ) 