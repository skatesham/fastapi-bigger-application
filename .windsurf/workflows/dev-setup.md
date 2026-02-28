---
description: Setup development environment and start the FastAPI server
---

# Development Setup Workflow

## 1. Install Dependencies
```bash
pip install -r requirements.txt
```

## 2. Setup Environment
```bash
cp .env.example .env
# Edit .env with your database credentials
```

## 3. Database Setup
```bash
# Generate initial migration
docker compose up db -d
alembic revision --autogenerate -m "Initial migration"

# Apply migrations
alembic upgrade head
```

## 4. Start Development Server
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## 5. Verify Setup
- Open http://localhost:8000/docs for Swagger UI
- Check health endpoint: http://localhost:8000/health
- Run tests: pytest

## Notes
- Make sure PostgreSQL is running
- Check .env configuration
- Verify database connection before starting server
