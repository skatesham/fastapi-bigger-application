---
description: Run tests and ensure code quality
---

# Testing Workflow

## 1. Run All Tests
```bash
pytest
```

## 2. Run with Coverage
```bash
pytest --cov=app --cov-report=html
```

## 3. Run Specific Test File
```bash
pytest tests/test_api/test_cars.py -v
```

## 4. Run Tests by Marker
```bash
pytest -m unit
pytest -m integration
```

## 5. Code Quality Checks
```bash
# Format code
black app/ tests/
isort app/ tests/

# Lint code
flake8 app/ tests/
mypy app/
```

## 6. Database Tests
```bash
# Run tests with test database
TEST_DATABASE_URL=postgresql://test:test@localhost/test_db pytest
```

## 7. Performance Tests
```bash
# Run load tests if available
pytest tests/performance/
```

## Test Categories

### Unit Tests
- Test individual functions
- Mock external dependencies
- Fast and isolated

### Integration Tests
- Test API endpoints
- Use test database
- Test complete flows

### E2E Tests
- Test complete user journeys
- Use real database
- Slower but comprehensive

## Coverage Requirements
- Minimum 80% coverage
- Focus on critical paths
- All endpoints tested
- Error scenarios covered

## Troubleshooting
- Check database connection for integration tests
- Verify test fixtures are properly loaded
- Ensure async tests use proper test client
