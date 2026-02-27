---
description: Create new API endpoint with proper structure
---

# Create New Endpoint Workflow

## 1. Add Response Messages to strings.py
```bash
# Add to app/resources/strings.py
# Errors - Resource Not Found (404)
RESOURCE_DOES_NOT_EXIST_ERROR = "resource does not exist"

# Errors - Resource Already Exists (409)
RESOURCE_ALREADY_EXISTS_ERROR = "resource already exists"

# Errors - Invalid Data (400)
INVALID_RESOURCE_ERROR = "Invalid resource data"

# Success Messages
RESOURCE_CREATED_SUCCESS = "Resource created successfully"
```

## 2. Create Pydantic Models
```bash
# Create domain models in app/src/domain/
touch app/src/domain/{resource}.py
```

## 3. Create Database Model
```bash
# Add SQLAlchemy model
# Include in app/src/domain/models.py or separate file
```

## 4. Create Service Layer
```bash
# Create service in app/src/core/
touch app/src/core/{resource}_service.py
```

## 5. Create API Endpoint
```bash
# Create endpoint file
touch app/src/api/v1/endpoints/{resource}.py
```

## 6. Update Router
```bash
# Add to app/src/api/v1/api.py
# Import and include new router
```

## 7. Create Tests
```bash
# Create test file
touch tests/test_api/test_{resource}.py
```

## 8. Generate Migration
```bash
alembic revision --autogenerate -m "Add {resource} table"
alembic upgrade head
```

## Template Files

### Endpoint Structure
```python
from fastapi import APIRouter, Depends, HTTPException
from app.resources.strings import (
    RESOURCE_DOES_NOT_EXIST_ERROR,
    RESOURCE_ALREADY_EXISTS_ERROR,
    INVALID_RESOURCE_ERROR
)
from typing import List

router = APIRouter()

@router.get("/{resource}", response_model=List[ResourceResponse])
async def get_{resource}s():
    pass

@router.post("/{resource}", response_model=ResourceResponse)
async def create_{resource}(resource: ResourceCreate):
    try:
        return resource_service.create_resource(resource)
    except ResourceAlreadyExistsError:
        raise HTTPException(status_code=409, detail=RESOURCE_ALREADY_EXISTS_ERROR)
    except InvalidResourceError:
        raise HTTPException(status_code=400, detail=INVALID_RESOURCE_ERROR)
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

def test_create_{resource}():
    response = client.post("/api/v1/{resource}", json={})
    assert response.status_code == 200
```

## String Usage Patterns

### Import Strings
```python
from app.resources.strings import (
    RESOURCE_DOES_NOT_EXIST_ERROR,
    RESOURCE_ALREADY_EXISTS_ERROR,
    RESOURCE_CREATED_SUCCESS
)
```

### Use in HTTP Exceptions
```python
# 404 Not Found
raise HTTPException(status_code=404, detail=RESOURCE_DOES_NOT_EXIST_ERROR)

# 409 Conflict
raise HTTPException(status_code=409, detail=RESOURCE_ALREADY_EXISTS_ERROR)

# 400 Bad Request
raise HTTPException(status_code=400, detail=INVALID_RESOURCE_ERROR)

# 422 Unprocessable Entity
raise HTTPException(status_code=422, detail=BUSINESS_LOGIC_ERROR)
```

### Use in Success Responses
```python
return {
    "message": RESOURCE_CREATED_SUCCESS,
    "data": resource_response
}
```

## Checklist
- [ ] Add response messages to strings.py
- [ ] Pydantic models created
- [ ] Database model added
- [ ] Service layer implemented
- [ ] API endpoint created with proper string usage
- [ ] Router updated
- [ ] Tests written
- [ ] Migration generated and applied
- [ ] All HTTP exceptions use centralized strings
