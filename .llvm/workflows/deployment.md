---
description: Deploy FastAPI application to production
---

# Deployment Workflow

## 1. Build Application
```bash
# Install production dependencies
pip install -r requirements.txt

# Run tests
pytest

# Check code quality
black app/
mypy app/
```

## 2. Database Migration
```bash
# Backup current database
pg_dump dbname > backup.sql

# Run migrations
alembic upgrade head
```

## 3. Environment Setup
```bash
# Set production environment variables
export ENVIRONMENT=production
export DATABASE_URL=postgresql://...
export SECRET_KEY=your-secret-key
```

## 4. Start Application
```bash
# Using Gunicorn (recommended)
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker

# Or using uvicorn directly
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## 5. Docker Deployment
```bash
# Build image
docker build -t fastapi-app .

# Run container
docker run -d -p 8000:8000 --env-file .env fastapi-app
```

## 6. Health Check
```bash
# Verify application is running
curl http://localhost:8000/health

# Check logs
docker logs <container_id>
```

## Production Checklist
- [ ] All tests passing
- [ ] Database migrations applied
- [ ] Environment variables set
- [ ] HTTPS configured
- [ ] Logging enabled
- [ ] Monitoring setup
- [ ] Backup strategy in place
- [ ] Security headers configured

## Monitoring
- Check application logs
- Monitor database connections
- Track API response times
- Set up alerts for errors

## Security
- Use HTTPS in production
- Set secure CORS policies
- Implement rate limiting
- Keep dependencies updated
- Use environment variables for secrets
