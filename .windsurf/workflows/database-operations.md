---
description: Database schema operations - add/remove columns, create domains
---

# Database Operations Workflow

## 1. Add Attribute to Table

### 1.1 Update SQLAlchemy Model
```python
# In app/src/domain/models.py
class Car(Base):
    __tablename__ = "cars"
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    # NEW ATTRIBUTE
    color = Column(String, nullable=True)  # Add this line
```

### 1.2 Update Pydantic Models
```python
# In app/src/domain/car.py
class CarBase(BaseModel):
    name: str
    color: Optional[str] = None  # Add this line

class CarCreate(CarBase):
    pass

class CarResponse(CarBase):
    id: int
    created_at: datetime
```

### 1.3 Generate Migration
```bash
# Generate migration for new column
alembic revision --autogenerate -m "Add color column to cars table"

# Apply migration
alembic upgrade head
```

## 2. Remove Attribute from Table

### 2.1 Update SQLAlchemy Model
```python
# In app/src/domain/models.py
class Car(Base):
    __tablename__ = "cars"
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    # REMOVED: color = Column(String, nullable=True)
```

### 2.2 Update Pydantic Models
```python
# In app/src/domain/car.py
class CarBase(BaseModel):
    name: str
    # REMOVED: color: Optional[str] = None
```

### 2.3 Generate Migration
```bash
# Generate migration to drop column
alembic revision --autogenerate -m "Remove color column from cars table"

# Apply migration
alembic upgrade head
```

## 3. Create New Domain/Entity

### 3.1 Create SQLAlchemy Model
```python
# In app/src/domain/models.py (or new file)
class Category(Base):
    __tablename__ = "categories"
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
```

### 3.2 Create Pydantic Models
```python
# Create app/src/domain/category.py
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class CategoryBase(BaseModel):
    name: str
    description: Optional[str] = None

class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

class CategoryResponse(CategoryBase):
    id: int
    created_at: datetime
```

### 3.3 Create Service Layer
```python
# Create app/src/core/category_service.py
from sqlalchemy.ext.asyncio import AsyncSession
from app.domain.models import Category
from app.domain.category import CategoryCreate, CategoryResponse

class CategoryService:
    async def create_category(
        self, 
        category: CategoryCreate, 
        db: AsyncSession
    ) -> CategoryResponse:
        # Implementation
        pass
```

### 3.4 Create API Endpoint
```python
# Create app/src/api/v1/endpoints/categories.py
from fastapi import APIRouter, Depends
from app.core.category_service import CategoryService
from app.domain.category import CategoryCreate, CategoryResponse

router = APIRouter()

@router.post("/categories", response_model=CategoryResponse)
async def create_category(
    category: CategoryCreate,
    service: CategoryService = Depends()
):
    return await service.create_category(category, db)
```

### 3.5 Update Router
```python
# In app/src/api/v1/api.py
from app.api.v1.endpoints import categories

api_router.include_router(categories.router, prefix="/categories", tags=["categories"])
```

### 3.6 Generate Migration
```bash
# Generate migration for new table
alembic revision --autogenerate -m "Create categories table"

# Apply migration
alembic upgrade head
```

## 4. Create Tests for New Domain
```python
# Create tests/test_api/test_categories.py
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_category():
    response = client.post(
        "/api/v1/categories",
        json={"name": "Test Category", "description": "Test description"}
    )
    assert response.status_code == 200
    assert response.json()["name"] == "Test Category"
```

## 5. Update Relationships (if needed)
```python
# Add foreign key relationships
class Car(Base):
    __tablename__ = "cars"
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"))
    category = relationship("Category", back_populates="cars")

class Category(Base):
    __tablename__ = "categories"
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    cars = relationship("Car", back_populates="category")
```

## Checklist for Database Changes
- [ ] Update SQLAlchemy models
- [ ] Update Pydantic models
- [ ] Update service layer
- [ ] Update API endpoints (if needed)
- [ ] Generate and apply migration
- [ ] Write/update tests
- [ ] Test in development environment
- [ ] Verify data integrity

## Important Notes
- Always backup database before applying migrations
- Test migrations on development first
- Use nullable=True for new columns to avoid breaking existing data
- Consider data migration for required columns
- Update API documentation after changes
