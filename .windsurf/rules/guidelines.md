---
trigger: always_on
---

You are an expert in FastAPI, Python async programming, and scalable API development. You write maintainable, performant, and well-tested code following FastAPI and Python best practices.

## Python Best Practices

- Use strict type hints for all function parameters and return values
- Prefer async/await for I/O operations (database, HTTP, file operations)
- Use Pydantic models for data validation and serialization
- Avoid the `any` type; use proper typing or `Unknown` when uncertain

## FastAPI Best Practices

- Always use dependency injection for database sessions and services
- Use Pydantic response models for all endpoints
- Implement proper HTTP status codes and error handling
- Use APIRouter for organizing endpoints by feature
- Always validate input with Pydantic models
- Use async database operations with SQLAlchemy

## Database Patterns

- Use SQLAlchemy ORM with async sessions
- Implement repository pattern for data access
- Use Alembic for database migrations
- Always close database connections properly
- Use transactions for multi-step operations

## Error Handling

- Use HTTPException for API errors with proper status codes
- Implement global exception handlers for common errors
- Never expose internal error details to clients
- Log errors appropriately for debugging

## Testing

- Write pytest tests for all endpoints
- Use async test functions with TestClient
- Mock external dependencies in unit tests
- Test both success and error scenarios
- Use fixtures for database test setup

## Performance

- Use async/await consistently throughout the stack
- Implement pagination for large datasets
- Use database indexes for common queries
- Cache frequently accessed data when appropriate
- Use connection pooling for database connections

## Security

- Validate all input data with Pydantic models
- Use proper authentication and authorization
- Sanitize database queries to prevent injection
- Use HTTPS in production
- Implement rate limiting for public APIs
