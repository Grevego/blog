"""
Seed data script for populating the database with test data.
Run with: python -m app.seed_data
"""

import os
import sys
from datetime import date, datetime, timedelta
from uuid import uuid4
from sqlalchemy.orm import Session

# Add the current directory to Python path to allow imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.database import SessionLocal, engine
from app.models.base import Base
from app.models.user import User
from app.models.category import Category
from app.models.post import Post
from app.services.user_service import user_service


def create_seed_data():
    """Create seed data for development and testing."""
    print("🌱 Starting seed data creation...")
    
    # Create all tables
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        # Clear existing data
        print("🗑️  Clearing existing data...")
        db.query(Post).delete()
        db.query(Category).delete()
        db.query(User).delete()
        db.commit()
        
        # Create dummy users
        print("👥 Creating dummy users...")
        users_data = [
            {
                "username": "johndoe",
                "email": "john.doe@example.com",
                "full_name": "John Doe",
                "bio": "Tech enthusiast and developer. Love writing about modern web technologies.",
                "avatar_url": "https://avatar.iran.liara.run/public/7",
                "website_url": "https://johndoe.dev",
                "password": "secretpassword123"
            },
            {
                "username": "janescience",
                "email": "jane.smith@example.com", 
                "full_name": "Jane Smith",
                "bio": "Data scientist and AI researcher. Passionate about machine learning.",
                "avatar_url": "https://avatar.iran.liara.run/public/2",
                "website_url": "https://janescience.com",
                "password": "anotherpassword456"
            },
            {
                "username": "devblogger",
                "email": "alex.wilson@example.com",
                "full_name": "Alex Wilson", 
                "bio": "Full-stack developer sharing knowledge about web development.",
                "avatar_url": "https://avatar.iran.liara.run/public/12",
                "website_url": "https://alexcode.blog",
                "password": "devpassword789"
            }
        ]
        
        users = []
        for user_data in users_data:
            password = user_data.pop("password")
            hashed_password = user_service._hash_password(password)
            user = User(**user_data, hashed_password=hashed_password)
            db.add(user)
            users.append(user)
        
        db.commit()
        print(f"✅ Created {len(users)} users")
        
        # Create dummy categories
        print("📂 Creating categories...")
        categories_data = [
            {
                "name": "Technology",
                "slug": "technology",
                "description": "Latest trends and insights in technology",
                "color": "#3B82F6"
            },
            {
                "name": "Web Development",
                "slug": "web-development", 
                "description": "Tips, tutorials, and best practices for web developers",
                "color": "#10B981"
            },
            {
                "name": "Machine Learning",
                "slug": "machine-learning",
                "description": "AI and ML tutorials, research, and applications", 
                "color": "#8B5CF6"
            },
            {
                "name": "Python",
                "slug": "python",
                "description": "Python programming tutorials and projects",
                "color": "#F59E0B"
            },
            {
                "name": "FastAPI",
                "slug": "fastapi",
                "description": "FastAPI framework guides and examples",
                "color": "#EF4444"
            },
            {
                "name": "Career",
                "slug": "career",
                "description": "Career advice and professional development",
                "color": "#6366F1"
            }
        ]
        
        categories = []
        for cat_data in categories_data:
            category = Category(**cat_data)
            db.add(category)
            categories.append(category)
        
        db.commit()
        print(f"✅ Created {len(categories)} categories")
        
        # Create dummy posts
        print("📝 Creating blog posts...")
        posts_data = [
            {
                "title": "Getting Started with FastAPI: A Complete Guide",
                "slug": "getting-started-fastapi-complete-guide",
                "excerpt": "Learn how to build modern REST APIs with FastAPI, from basic setup to advanced features.",
                "content": """# Getting Started with FastAPI

FastAPI is a modern, fast (high-performance), web framework for building APIs with Python 3.7+ based on standard Python type hints.

## Why FastAPI?

- **Fast**: Very high performance, on par with NodeJS and Go
- **Fast to code**: Increase the speed to develop features by about 200% to 300%
- **Fewer bugs**: Reduce about 40% of human (developer) induced errors
- **Intuitive**: Great editor support with completion everywhere
- **Easy**: Designed to be easy to use and learn
- **Short**: Minimize code duplication

## Installation

```bash
pip install fastapi uvicorn
```

## Your First API

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}
```

This creates a simple API that you can run with:

```bash
uvicorn main:app --reload
```

## What's Next?

In upcoming posts, we'll dive deeper into:
- Request validation with Pydantic
- Database integration with SQLAlchemy
- Authentication and authorization
- Testing FastAPI applications""",
                "author": users[0],
                "categories": [categories[1], categories[4]],  # Web Development, FastAPI
                "is_published": True,
                "is_featured": True,
                "published_at": date.today() - timedelta(days=2),
                "meta_title": "FastAPI Complete Guide - Build Modern APIs",
                "meta_description": "Learn FastAPI from scratch with this comprehensive guide covering installation, basic usage, and advanced features."
            },
            {
                "title": "Machine Learning Model Deployment with Python",
                "slug": "ml-model-deployment-python",
                "excerpt": "A practical guide to deploying machine learning models in production using Python and modern MLOps practices.",
                "content": """# Deploying Machine Learning Models

Model deployment is often the most challenging part of the ML lifecycle. Here's how to do it right.

## Deployment Strategies

### 1. Batch Prediction
- Schedule regular predictions
- Good for large datasets
- Lower latency requirements

### 2. Real-time API
- Instant predictions
- RESTful endpoints
- Higher availability needs

### 3. Streaming
- Process data as it arrives
- Apache Kafka or similar
- Complex but powerful

## Tools and Frameworks

**Containerization:**
- Docker for packaging
- Kubernetes for orchestration

**Model Serving:**
- FastAPI for REST APIs
- TensorFlow Serving
- MLflow

**Monitoring:**
- Data drift detection
- Model performance tracking
- Alert systems

## Best Practices

1. **Version Control**: Track model versions
2. **Testing**: Validate before deployment
3. **Monitoring**: Watch performance metrics
4. **Rollback**: Quick recovery plans

Stay tuned for hands-on tutorials!""",
                "author": users[1],
                "categories": [categories[2], categories[3]],  # ML, Python
                "is_published": True,
                "is_featured": True,
                "published_at": date.today() - timedelta(days=5),
                "meta_title": "ML Model Deployment Guide | Production Ready",
                "meta_description": "Deploy machine learning models in production with Python. Learn containerization, monitoring, and best practices."
            },
            {
                "title": "Database Migrations with Alembic: Best Practices",
                "slug": "database-migrations-alembic-best-practices",
                "excerpt": "Master database migrations with Alembic. Learn migration strategies, rollback procedures, and production deployment tips.",
                "content": """# Database Migrations with Alembic

Database migrations are crucial for maintaining data integrity while evolving your application schema.

## What is Alembic?

Alembic is a lightweight database migration tool for usage with SQLAlchemy. It provides:
- Version control for database schema
- Automatic migration generation
- Safe rollback capabilities

## Setting Up Alembic

```bash
# Initialize Alembic
alembic init alembic

# Generate migration
alembic revision --autogenerate -m "Add user table"

# Apply migration
alembic upgrade head
```

## Migration Best Practices

### 1. Review Auto-generated Migrations
Always review what Alembic generates:
- Check for data loss operations
- Verify constraint changes
- Test with sample data

### 2. Handle Data Migration
Sometimes you need to migrate data too:

```python
def upgrade():
    # Schema changes first
    op.add_column('users', sa.Column('full_name', sa.String(255)))
    
    # Then data migration
    connection = op.get_bind()
    connection.execute(
        "UPDATE users SET full_name = first_name || ' ' || last_name"
    )
```

### 3. Backward Compatibility
Plan for rollbacks:
- Test downgrade operations
- Consider data preservation
- Document breaking changes

## Production Deployment

1. **Backup First**: Always backup before migrations
2. **Test Migrations**: Run on staging environment
3. **Monitor Performance**: Watch for long-running operations
4. **Have Rollback Plan**: Know how to revert quickly

## Common Pitfalls

- Not handling NULL values in new columns
- Forgetting to update indexes
- Large table migrations without batching
- Not testing rollback procedures

Happy migrating! 🚀""",
                "author": users[2],
                "categories": [categories[1], categories[3]],  # Web Development, Python
                "is_published": True,
                "is_featured": False,
                "published_at": date.today() - timedelta(days=1),
                "meta_title": "Alembic Migration Best Practices",
                "meta_description": "Learn database migration best practices with Alembic including safe deployment strategies and rollback procedures."
            },
            {
                "title": "Building a Career in Tech: 2024 Developer Roadmap",
                "slug": "tech-career-2024-developer-roadmap",
                "excerpt": "Navigate your tech career with our 2024 roadmap. From learning paths to salary negotiations, everything you need to succeed.",
                "content": """# Tech Career Roadmap 2024

The tech industry continues to evolve rapidly. Here's your guide to building a successful career.

## Learning Paths

### Frontend Development
- **Essential**: HTML, CSS, JavaScript
- **Frameworks**: React, Vue, or Angular
- **Tools**: Webpack, Vite, TypeScript
- **Trending**: Next.js, Svelte, Web3

### Backend Development  
- **Languages**: Python, Node.js, Go, Rust
- **Databases**: PostgreSQL, MongoDB, Redis
- **Cloud**: AWS, GCP, Azure
- **DevOps**: Docker, Kubernetes, CI/CD

### Full-Stack
Combine frontend and backend skills with:
- API design and implementation
- Database modeling
- System architecture
- Performance optimization

## Skill Development Strategy

### 1. Master the Fundamentals
Don't skip the basics:
- Data structures and algorithms
- System design principles
- Clean code practices
- Testing methodologies

### 2. Build Projects
Portfolio projects demonstrate skills:
- Personal projects show passion
- Open source contributions build community
- Freelance work provides experience

### 3. Stay Current
- Follow tech blogs and newsletters
- Attend conferences and meetups
- Take online courses
- Experiment with new technologies

## Career Advancement

### Junior → Mid-Level (1-3 years)
- Focus on code quality
- Learn debugging skills
- Understand business requirements
- Mentor newer developers

### Mid-Level → Senior (3-5 years)
- System design skills
- Architecture decisions
- Cross-team collaboration
- Technical leadership

### Senior → Staff/Principal (5+ years)
- Strategic technical vision
- Mentoring and coaching
- Process improvement
- Technology evaluation

## Salary Negotiation Tips

1. **Research Market Rates**: Use sites like Glassdoor, levels.fyi
2. **Document Achievements**: Quantify your impact
3. **Consider Total Compensation**: Equity, benefits, PTO
4. **Practice Your Pitch**: Rehearse your value proposition
5. **Know Your Worth**: Don't undervalue your skills

## Remote Work Trends

Post-2024 considerations:
- Hybrid work models
- Async communication skills
- Global talent competition
- Work-life balance importance

## Conclusion

Success in tech requires continuous learning, building great relationships, and staying adaptable. Focus on solving real problems and the opportunities will follow.

What's your next career move? 🚀""",
                "author": users[0],
                "categories": [categories[5], categories[0]],  # Career, Technology
                "is_published": True,
                "is_featured": False,
                "published_at": date.today() - timedelta(days=3),
                "meta_title": "2024 Tech Career Roadmap | Developer Guide",
                "meta_description": "Complete 2024 tech career guide covering learning paths, skill development, and salary negotiation for developers."
            },
            {
                "title": "Advanced Python Decorators: Beyond the Basics",
                "slug": "advanced-python-decorators-beyond-basics",
                "excerpt": "Dive deep into Python decorators with advanced patterns, class decorators, and real-world use cases.",
                "content": """# Advanced Python Decorators

Decorators are one of Python's most powerful features. Let's explore advanced patterns beyond basic function decoration.

## Decorator Fundamentals Recap

```python
def my_decorator(func):
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__}")
        result = func(*args, **kwargs)
        print(f"Finished {func.__name__}")
        return result
    return wrapper

@my_decorator
def greet(name):
    return f"Hello, {name}!"
```

## Advanced Patterns

### 1. Parametrized Decorators

```python
def retry(max_attempts=3, delay=1):
    def decorator(func):
        def wrapper(*args, **kwargs):
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts - 1:
                        raise e
                    time.sleep(delay)
        return wrapper
    return decorator

@retry(max_attempts=5, delay=2)
def unreliable_api_call():
    # Might fail sometimes
    pass
```

### 2. Class Decorators

```python
def singleton(cls):
    instances = {}
    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return get_instance

@singleton
class DatabaseConnection:
    def __init__(self):
        self.connection = "connected"
```

### 3. Property Decorators

```python
class Circle:
    def __init__(self, radius):
        self._radius = radius
    
    @property
    def radius(self):
        return self._radius
    
    @radius.setter
    def radius(self, value):
        if value < 0:
            raise ValueError("Radius cannot be negative")
        self._radius = value
    
    @property
    def area(self):
        return 3.14159 * self._radius ** 2
```

## Real-World Use Cases

### 1. Caching/Memoization

```python
from functools import wraps
import time

def memoize(func):
    cache = {}
    
    @wraps(func)
    def wrapper(*args, **kwargs):
        key = str(args) + str(sorted(kwargs.items()))
        if key not in cache:
            cache[key] = func(*args, **kwargs)
        return cache[key]
    return wrapper

@memoize
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n-1) + fibonacci(n-2)
```

### 2. Authentication/Authorization

```python
def require_auth(role=None):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Check authentication
            if not current_user.is_authenticated:
                raise AuthenticationError("Login required")
            
            # Check authorization
            if role and not current_user.has_role(role):
                raise AuthorizationError(f"Role '{role}' required")
            
            return func(*args, **kwargs)
        return wrapper
    return decorator

@require_auth(role='admin')
def delete_user(user_id):
    # Only admins can delete users
    pass
```

### 3. Performance Monitoring

```python
def monitor_performance(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        start_memory = get_memory_usage()
        
        try:
            result = func(*args, **kwargs)
            return result
        finally:
            execution_time = time.time() - start_time
            memory_used = get_memory_usage() - start_memory
            
            logger.info(f"{func.__name__} took {execution_time:.2f}s")
            logger.info(f"{func.__name__} used {memory_used}MB")
    
    return wrapper
```

## Best Practices

1. **Use `functools.wraps`**: Preserves original function metadata
2. **Handle edge cases**: Consider what happens with exceptions
3. **Keep it simple**: Don't over-engineer decorators
4. **Document behavior**: Make decorator effects clear
5. **Test thoroughly**: Decorators can be tricky to debug

## Common Pitfalls

- Not preserving function signatures
- Creating memory leaks with closures
- Overusing decorators (readability)
- Not handling exceptions properly

Decorators are powerful but should be used judiciously! 🐍""",
                "author": users[1],
                "categories": [categories[3]],  # Python
                "is_published": True,
                "is_featured": False,
                "published_at": date.today(),
                "meta_title": "Advanced Python Decorators Tutorial",
                "meta_description": "Master advanced Python decorator patterns including parametrized decorators, class decorators, and real-world examples."
            },
            {
                "title": "Building Scalable Web APIs: Architecture Principles",
                "slug": "scalable-web-apis-architecture-principles",
                "excerpt": "Learn the fundamental principles for designing and building scalable web APIs that can handle millions of requests.",
                "content": """# Scalable Web API Architecture

Building APIs that scale requires careful planning and adherence to key architectural principles.

## Core Principles

### 1. Statelessness
Each request should contain all necessary information:
- No server-side session storage
- Use tokens for authentication
- Enables horizontal scaling

### 2. Idempotency
Safe operations should be repeatable:
- GET, PUT, DELETE should be idempotent
- Use idempotency keys for POST requests
- Prevents duplicate processing

### 3. Versioning Strategy
Plan for API evolution:
- URL versioning: `/api/v1/users`
- Header versioning: `Accept: application/vnd.api+json;version=1`
- Query parameter: `/api/users?version=1`

## Scaling Patterns

### Horizontal Scaling
- Load balancers distribute traffic
- Multiple server instances
- Database read replicas
- Microservices architecture

### Caching Strategies
- **Client-side**: Browser caching
- **CDN**: Global content distribution
- **Application**: Redis/Memcached
- **Database**: Query result caching

### Database Optimization
- Proper indexing
- Connection pooling
- Query optimization
- Database sharding

## Performance Optimization

### 1. Response Time
```python
# Use async/await for I/O operations
async def get_user_data(user_id):
    user = await db.get_user(user_id)
    posts = await db.get_user_posts(user_id)
    return {"user": user, "posts": posts}
```

### 2. Pagination
```python
# Cursor-based pagination for large datasets
@app.get("/posts")
def get_posts(cursor: str = None, limit: int = 20):
    posts = db.get_posts_after_cursor(cursor, limit)
    next_cursor = posts[-1].id if posts else None
    return {
        "posts": posts,
        "next_cursor": next_cursor,
        "has_more": len(posts) == limit
    }
```

### 3. Rate Limiting
```python
from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter

@app.get("/api/data")
@app.depends(RateLimiter(times=100, seconds=60))
def get_data():
    return {"data": "value"}
```

## Monitoring and Observability

### Key Metrics
- Response time (p50, p95, p99)
- Throughput (requests per second)
- Error rates
- Resource utilization

### Logging Strategy
```python
import structlog

logger = structlog.get_logger()

@app.middleware("http")
async def log_requests(request, call_next):
    start_time = time.time()
    
    response = await call_next(request)
    
    duration = time.time() - start_time
    logger.info(
        "Request processed",
        method=request.method,
        url=str(request.url),
        status_code=response.status_code,
        duration=duration
    )
    
    return response
```

## Security Considerations

### 1. Authentication & Authorization
- JWT tokens with proper expiration
- OAuth 2.0 for third-party access
- Role-based access control

### 2. Input Validation
```python
from pydantic import BaseModel, validator

class UserCreate(BaseModel):
    email: str
    password: str
    
    @validator('email')
    def validate_email(cls, v):
        if '@' not in v:
            raise ValueError('Invalid email')
        return v.lower()
    
    @validator('password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('Password too short')
        return v
```

### 3. Data Protection
- HTTPS everywhere
- Sensitive data encryption
- SQL injection prevention
- CORS configuration

## Error Handling

### Consistent Error Format
```python
class APIError(Exception):
    def __init__(self, status_code, message, details=None):
        self.status_code = status_code
        self.message = message
        self.details = details

@app.exception_handler(APIError)
async def api_error_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "message": exc.message,
                "details": exc.details,
                "timestamp": datetime.utcnow().isoformat()
            }
        }
    )
```

## Testing Strategy

### 1. Unit Tests
Test individual components in isolation

### 2. Integration Tests
Test API endpoints with real database

### 3. Load Testing
```bash
# Using Artillery.js
artillery quick --count 100 --num 10 http://localhost:8000/api/posts
```

## Deployment Best Practices

1. **Containerization**: Docker for consistency
2. **Infrastructure as Code**: Terraform/CloudFormation
3. **Blue-Green Deployment**: Zero-downtime updates
4. **Health Checks**: Kubernetes readiness/liveness probes
5. **Auto-scaling**: Based on CPU/memory/custom metrics

## Conclusion

Scalable API design is about making the right trade-offs and planning for growth. Start simple, measure everything, and optimize based on real data.

Remember: premature optimization is the root of all evil, but planning for scale is essential! 🚀""",
                "author": users[2],
                "categories": [categories[1], categories[0]],  # Web Development, Technology
                "is_published": False,  # Draft post
                "is_featured": False,
                "published_at": None,
                "meta_title": "Scalable Web API Architecture Guide",
                "meta_description": "Learn to build scalable web APIs with proper architecture, caching, monitoring, and security best practices."
            }
        ]
        
        for post_data in posts_data:
            # Extract categories and author from the data
            categories_for_post = post_data.pop("categories")
            author = post_data.pop("author")
            
            # Create the post
            post = Post(**post_data, author_id=author.id)
            post.categories = categories_for_post
            
            db.add(post)
        
        db.commit()
        print(f"✅ Created {len(posts_data)} blog posts")
        
        # Print summary
        print("\n📊 Seed data summary:")
        print(f"   👥 Users: {len(users)}")
        print(f"   📂 Categories: {len(categories)}")
        print(f"   📝 Posts: {len(posts_data)}")
        print(f"   🌟 Featured posts: {sum(1 for p in posts_data if p.get('is_featured'))}")
        print(f"   📖 Published posts: {sum(1 for p in posts_data if p.get('is_published'))}")
        
        print("\n🔗 Test URLs:")
        print("   📋 All posts: http://localhost:8000/api/v1/posts/")
        print("   🌟 Featured: http://localhost:8000/api/v1/posts/featured")
        print("   👥 Users: http://localhost:8000/api/v1/users/")
        print("   📂 Categories: http://localhost:8000/api/v1/categories/")
        print("   📚 API Docs: http://localhost:8000/docs")
        
        print("\n✨ Seed data creation completed successfully!")
        
    except Exception as e:
        print(f"❌ Error creating seed data: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    create_seed_data() 