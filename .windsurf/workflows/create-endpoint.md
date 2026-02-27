---
description: Create new API endpoint with proper structure
---

# Create New Endpoint Workflow

## 1. Create Pydantic Models
```bash
# Create domain models in app/src/domain/
touch app/src/domain/{resource}.py
```

## 2. Create Database Model
```bash
# Add SQLAlchemy model
# Include in app/src/domain/models.py or separate file
```

## 3. Create Service Layer
```bash
# Create service in app/src/core/
touch app/src/core/{resource}_service.py
```

## 4. Create API Endpoint
```bash
# Create endpoint file
touch app/src/api/v1/endpoints/{resource}.py
```

## 5. Update Router
```bash
# Add to app/src/api/v1/api.py
# Import and include new router
```

## 6. Create Tests
```bash
# Create test file
touch tests/test_api/test_{resource}.py
```

## 7. Generate Migration
```bash
alembic revision --autogenerate -m "Add {resource} table"
alembic upgrade head
```

## Template Files

### Endpoint Structure
```python
from fastapi import APIRouter, Depends, HTTPException
from typing import List

router = APIRouter()

@router.get("/{resource}", response_model=List[ResourceResponse])
async def get_{resource}s():
    pass

@router.post("/{resource}", response_model=ResourceResponse)
async def create_{resource}(resource: ResourceCreate):
    pass
```

### Test Structure
```python
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_get_{resource}s():
    response = client.get("/api/v1/{resource}")
    assert response.status_code == 200
```

## Checklist
- [ ] Pydantic models created
- [ ] Database model added
- [ ] Service layer implemented
- [ ] API endpoint created
- [ ] Router updated
- [ ] Tests written
- [ ] Migration generated and applied
