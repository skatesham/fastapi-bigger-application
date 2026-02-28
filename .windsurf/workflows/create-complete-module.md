---
description: Create complete module with all layers following FastAPI best practices
---

# Create Complete Module Workflow

## Overview
This workflow creates a complete module with all required layers: models, schemas, repository, service, endpoints, and tests following the established patterns.

## 1. Module Structure Creation
```bash
# Create domain directory structure
mkdir -p app/src/domain/{module}
touch app/src/domain/{module}/__init__.py
touch app/src/domain/{module}/models.py
touch app/src/domain/{module}/schemas.py
touch app/src/domain/{module}/repository.py
touch app/src/domain/{module}/service.py
touch app/src/domain/{module}/exceptions.py

# Create API endpoint
touch app/src/api/v1/endpoints/{module}.py

# Create tests
touch tests/test_api/test_{module}.py
touch tests/test_{module}.py
```

## 2. Add Response Messages to strings.py
```python
# Add to app/resources/strings.py
# Errors - Resource Not Found (404)
{MODULE}_DOES_NOT_EXIST_ERROR = "{module} does not exist"

# Errors - Resource Already Exists (409)
{MODULE}_ALREADY_EXISTS_ERROR = "{module} already exists"

# Errors - Invalid Data (400)
INVALID_{MODULE}_ERROR = "Invalid {module} data"

# Success Messages
{MODULE}_CREATED_SUCCESS = "{module} created successfully"
{MODULE}_UPDATED_SUCCESS = "{module} updated successfully"
{MODULE}_DELETED_SUCCESS = "{module} deleted successfully"
```

## 3. Database Model (models.py)
```python
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.sql import func
from app.src.core.database import Base

class {Model}(Base):
    __tablename__ = "{module}s"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    # Add other fields as needed
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    def __repr__(self):
        return f"<{Model}(id={self.id}, name={self.name})>"
```

## 4. Pydantic Schemas (schemas.py)
```python
from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

class {Model}Base(BaseModel):
    name: str
    # Add other fields as needed

class {Model}Create({Model}Base):
    pass

class {Model}Update(BaseModel):
    name: Optional[str] = None
    # Add other optional fields as needed

class {Model}({Model}Base):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
```

## 5. Custom Exceptions (exceptions.py)
```python
class {Module}NotFoundError(Exception):
    def __init__(self, module_id: int):
        self.module_id = module_id
        super().__init__(f"{Module} with ID {module_id} not found")

class {Module}AlreadyExistsError(Exception):
    def __init__(self, field: str, value: str):
        self.field = field
        self.value = value
        super().__init__(f"{Module} with {field} '{value}' already exists")
```

## 6. Repository Layer (repository.py)
```python
from typing import List, Optional
from sqlalchemy.orm import Session
from app.src.core.database import get_database
from .models import {Model}
from .schemas import {Model}Create, {Model}Update

class {Model}Repository:
    def get_by_id(self, db: Session, id: int) -> Optional[{Model}]:
        return db.query({Model}).filter({Model}.id == id).first()
    
    def get_multi(self, db: Session, skip: int = 0, limit: int = 100) -> List[{Model}]:
        return db.query({Model}).offset(skip).limit(limit).all()
    
    def get_by_name(self, db: Session, name: str) -> Optional[{Model}]:
        return db.query({Model}).filter({Model}.name == name).first()
    
    def create(self, db: Session, *, obj_in: {Model}Create) -> {Model}:
        obj_data = obj_in.model_dump()
        db_obj = {Model}(**obj_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def update(self, db: Session, *, db_obj: {Model}, obj_in: {Model}Update) -> {Model}:
        obj_data = obj_in.model_dump(exclude_unset=True)
        for field, value in obj_data.items():
            setattr(db_obj, field, value)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def delete(self, db: Session, *, id: int) -> {Model}:
        obj = db.query({Model}).get(id)
        db.delete(obj)
        db.commit()
        return obj

# Create singleton instance
{module}_repository = {Model}Repository()
```

## 7. Service Layer (service.py)
```python
from typing import List
from sqlalchemy.orm import Session
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import select

from . import exceptions, repository, schemas
from .models import {Model}

class {Module}Service:
    def __init__(self):
        self.{module}_repository = repository.{module}_repository

    def create_{module}(self, db: Session, {module}: schemas.{Model}Create) -> schemas.{Model}:
        """Create a new {module}"""
        # Check if {module} with same name already exists
        existing_{module} = self.{module}_repository.get_by_name(db, name={module}.name)
        if existing_{module}:
            raise exceptions.{Module}AlreadyExistsError("name", {module}.name)
        
        # Create {module}
        db_{module} = self.{module}_repository.create(db, obj_in={module})
        return db_{module}

    def get_{module}(self, db: Session, {module}_id: int) -> schemas.{Model}:
        """Get {module} by ID"""
        db_{module} = self.{module}_repository.get_by_id(db, id={module}_id)
        if db_{module} is None:
            raise exceptions.{Module}NotFoundError({module}_id)
        
        return db_{module}

    def get_{module}s(self, db: Session) -> Page[schemas.{Model}]:
        """Get all {module}s with pagination"""
        return paginate(db, select({Model}).order_by({Model}.id))

    def update_{module}(self, db: Session, {module}_id: int, {module}_update: schemas.{Model}Update) -> schemas.{Model}:
        """Update {module}"""
        db_{module} = self.{module}_repository.get_by_id(db, id={module}_id)
        if db_{module} is None:
            raise exceptions.{Module}NotFoundError({module}_id)
        
        # Check if name is being updated and already exists
        if {module}_update.name and {module}_update.name != db_{module}.name:
            existing_{module} = self.{module}_repository.get_by_name(db, name={module}_update.name)
            if existing_{module}:
                raise exceptions.{Module}AlreadyExistsError("name", {module}_update.name)
        
        # Update {module}
        updated_{module} = self.{module}_repository.update(db, db_obj=db_{module}, obj_in={module}_update)
        return updated_{module}

    def delete_{module}(self, db: Session, {module}_id: int) -> bool:
        """Delete {module}"""
        try:
            self.{module}_repository.delete(db, id={module}_id)
            return True
        except ValueError:
            raise exceptions.{Module}NotFoundError({module}_id)

    def search_{module}s_by_name(self, db: Session, name: str) -> List[schemas.{Model}]:
        """Search {module}s by name"""
        db_{module}s = self.{module}_repository.get_by_name(db, name=name)
        return db_{module}s if db_{module}s else []

# Create singleton instance
{module}_service = {Module}Service()
```

## 8. API Endpoints (endpoints/{module}.py)
```python
from fastapi import APIRouter, HTTPException
from fastapi_pagination import Page
from typing import List

from app.src.api.deps import Database
from app.src.domain.{module} import exceptions, schemas
from app.src.domain.{module}.service import {module}_service
from app.resources.strings import (
    {MODULE}_DOES_NOT_EXIST_ERROR,
    {MODULE}_ALREADY_EXISTS_ERROR,
    INVALID_{MODULE}_ERROR
)

router = APIRouter()

@router.post("/", response_model=schemas.{Model}, status_code=201)
def create_{module}(
    {module}: schemas.{Model}Create,
    db: Database,
):
    """Create new {module} using dependency injection"""
    try:
        return {module}_service.create_{module}(db=db, {module}={module})
    except exceptions.{Module}AlreadyExistsError as e:
        raise HTTPException(status_code=409, detail={MODULE}_ALREADY_EXISTS_ERROR)

@router.get("/{{{module}_id}}", response_model=schemas.{Model})
def read_{module}(
    {module}_id: int,
    db: Database,
):
    """Get {module} by ID using dependency injection"""
    try:
        return {module}_service.get_{module}(db, {module}_id={module}_id)
    except exceptions.{Module}NotFoundError as e:
        raise HTTPException(status_code=404, detail={MODULE}_DOES_NOT_EXIST_ERROR)

@router.get("/", response_model=Page[schemas.{Model}])
def read_{module}s(
    db: Database,
):
    """Get all {module}s with automatic pagination"""
    return {module}_service.get_{module}s(db)

@router.put("/{{{module}_id}}", response_model=schemas.{Model})
def update_{module}(
    {module}_id: int,
    {module}_update: schemas.{Model}Update,
    db: Database,
):
    """Update {module} by ID using dependency injection"""
    try:
        return {module}_service.update_{module}(db, {module}_id={module}_id, {module}_update={module}_update)
    except exceptions.{Module}NotFoundError as e:
        raise HTTPException(status_code=404, detail={MODULE}_DOES_NOT_EXIST_ERROR)
    except exceptions.{Module}AlreadyExistsError as e:
        raise HTTPException(status_code=409, detail={MODULE}_ALREADY_EXISTS_ERROR)

@router.delete("/{{{module}_id}}", response_model=bool)
def delete_{module}(
    {module}_id: int,
    db: Database,
):
    """Delete {module} by ID using dependency injection"""
    try:
        return {module}_service.delete_{module}(db, {module}_id={module}_id)
    except exceptions.{Module}NotFoundError as e:
        raise HTTPException(status_code=404, detail={MODULE}_DOES_NOT_EXIST_ERROR)

@router.get("/search/", response_model=List[schemas.{Model}])
def search_{module}s(
    name: str,
    db: Database,
):
    """Search {module}s by name"""
    return {module}_service.search_{module}s_by_name(db, name=name)
```

## 9. Update Dependencies (deps.py)
```python
# Add to app/src/api/deps.py
from app.src.domain.{module}.service import {module}_service

# Add to Database dependency or create separate
def get_{module}_service() -> {Module}Service:
    return {module}_service
```

## 10. Update API Router (api.py)
```python
# Add to app/src/api/v1/api.py
from app.src.api.v1.endpoints import {module}

# Include router
api_router.include_router({module}.router, prefix="/{module}s", tags=["{module}s"])
```

## 11. Database Migration
```bash
# Generate migration
alembic revision --autogenerate -m "Add {module} table"

# Apply migration
alembic upgrade head
```

## 12. Tests
### API Tests (test_api/test_{module}.py)
```python
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.resources.strings import {MODULE}_DOES_NOT_EXIST_ERROR, {MODULE}_ALREADY_EXISTS_ERROR

client = TestClient(app)

def test_create_{module}():
    """Test creating a new {module}"""
    {module}_data = {
        "name": "Test {Module}"
    }
    response = client.post("/api/v1/{module}s/", json={module}_data)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == {module}_data["name"]
    assert "id" in data

def test_create_duplicate_{module}():
    """Test creating duplicate {module} raises error"""
    {module}_data = {
        "name": "Test {Module}"
    }
    # Create first {module}
    client.post("/api/v1/{module}s/", json={module}_data)
    # Try to create duplicate
    response = client.post("/api/v1/{module}s/", json={module}_data)
    assert response.status_code == 409
    assert response.json()["detail"] == {MODULE}_ALREADY_EXISTS_ERROR

def test_get_{module}():
    """Test getting {module} by ID"""
    # Create {module} first
    {module}_data = {"name": "Test {Module}"}
    create_response = client.post("/api/v1/{module}s/", json={module}_data)
    {module}_id = create_response.json()["id"]
    
    # Get {module}
    response = client.get(f"/api/v1/{module}s/{module}_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == {module}_id
    assert data["name"] == {module}_data["name"]

def test_get_nonexistent_{module}():
    """Test getting nonexistent {module} raises error"""
    response = client.get("/api/v1/{module}s/99999")
    assert response.status_code == 404
    assert response.json()["detail"] == {MODULE}_DOES_NOT_EXIST_ERROR

def test_get_{module}s():
    """Test getting all {module}s with pagination"""
    response = client.get("/api/v1/{module}s/")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert "total" in data
    assert "page" in data
    assert "size" in data

def test_update_{module}():
    """Test updating {module}"""
    # Create {module} first
    {module}_data = {"name": "Test {Module}"}
    create_response = client.post("/api/v1/{module}s/", json={module}_data)
    {module}_id = create_response.json()["id"]
    
    # Update {module}
    update_data = {"name": "Updated {Module}"}
    response = client.put(f"/api/v1/{module}s/{module}_id}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == update_data["name"]

def test_delete_{module}():
    """Test deleting {module}"""
    # Create {module} first
    {module}_data = {"name": "Test {Module}"}
    create_response = client.post("/api/v1/{module}s/", json={module}_data)
    {module}_id = create_response.json()["id"]
    
    # Delete {module}
    response = client.delete(f"/api/v1/{module}s/{module}_id}")
    assert response.status_code == 200
    assert response.json() is True

def test_search_{module}s():
    """Test searching {module}s by name"""
    # Create {module}s
    {module}_data1 = {"name": "Test {Module} 1"}
    {module}_data2 = {"name": "Test {Module} 2"}
    client.post("/api/v1/{module}s/", json={module}_data1)
    client.post("/api/v1/{module}s/", json={module}_data2)
    
    # Search {module}s
    response = client.get("/api/v1/{module}s/search/?name=Test")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 2
```

### Service Tests (test_{module}.py)
```python
import pytest
from sqlalchemy.orm import Session
from app.src.domain.{module} import service, schemas, exceptions
from app.src.domain.{module}.models import {Model}

def test_create_{module}(db_session: Session):
    """Test creating {module} in service layer"""
    {module}_data = schemas.{Model}Create(name="Test {Module}")
    result = service.{module}_service.create_{module}(db_session, {module}_data)
    
    assert result.name == {module}_data.name
    assert result.id is not None

def test_create_duplicate_{module}(db_session: Session):
    """Test creating duplicate {module} raises exception"""
    {module}_data = schemas.{Model}Create(name="Test {Module}")
    service.{module}_service.create_{module}(db_session, {module}_data)
    
    with pytest.raises(exceptions.{Module}AlreadyExistsError):
        service.{module}_service.create_{module}(db_session, {module}_data)

def test_get_{module}(db_session: Session):
    """Test getting {module} by ID"""
    {module}_data = schemas.{Model}Create(name="Test {Module}")
    created = service.{module}_service.create_{module}(db_session, {module}_data)
    
    result = service.{module}_service.get_{module}(db_session, created.id)
    assert result.id == created.id
    assert result.name == created.name

def test_get_nonexistent_{module}(db_session: Session):
    """Test getting nonexistent {module} raises exception"""
    with pytest.raises(exceptions.{Module}NotFoundError):
        service.{module}_service.get_{module}(db_session, 99999)
```

## 13. Update __init__.py Files
```python
# app/src/domain/{module}/__init__.py
from .models import {Model}
from .schemas import {Model}, {Model}Create, {Model}Update
from .service import {module}_service, {Module}Service
from .repository import {module}_repository, {Model}Repository
from . import exceptions

__all__ = [
    "{Model}",
    "{Model}Create", 
    "{Model}Update",
    "{module}_service",
    "{Module}Service",
    "{module}_repository",
    "{Model}Repository",
    "exceptions"
]
```

## Pattern Requirements

### Pagination Pattern
- **List endpoints**: Must use `Page[schemas.{Model}]` for automatic pagination
- **Search endpoints**: Can use `List[schemas.{Model}]` for filtered results
- **Service layer**: Use `paginate(db, select({Model}).order_by({Model}.id))`

### Response Model Pattern
- **Single item**: `schemas.{Model}`
- **List with pagination**: `Page[schemas.{Model}]`
- **Create**: `schemas.{Model}Create`
- **Update**: `schemas.{Model}Update`

### Error Handling Pattern
- **404 Not Found**: `HTTPException(status_code=404, detail={MODULE}_DOES_NOT_EXIST_ERROR)`
- **409 Conflict**: `HTTPException(status_code=409, detail={MODULE}_ALREADY_EXISTS_ERROR)`
- **400 Bad Request**: `HTTPException(status_code=400, detail=INVALID_{MODULE}_ERROR)`

### Dependency Injection Pattern
- **Database**: Use `Database` dependency from deps.py
- **Services**: Inject services through deps.py
- **Repositories**: Services manage repositories internally

## Checklist
- [ ] Module structure created
- [ ] Response messages added to strings.py
- [ ] Database model implemented
- [ ] Pydantic schemas created
- [ ] Custom exceptions defined
- [ ] Repository layer implemented
- [ ] Service layer implemented with pagination
- [ ] API endpoints created with proper response models
- [ ] Dependencies updated in deps.py
- [ ] Router updated in api.py
- [ ] Database migration generated and applied
- [ ] API tests written
- [ ] Service tests written
- [ ] __init__.py files updated
- [ ] All endpoints follow pagination patterns
- [ ] Error handling uses centralized strings
- [ ] Dependency injection properly implemented
