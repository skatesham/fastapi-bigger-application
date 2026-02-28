from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session
from typing import Dict, Any
from datetime import datetime, timezone

from ...deps import Database
from ....core.config import settings
from ....core.database import engine

router = APIRouter()


@router.get("/health", response_model=Dict[str, Any])
async def health_check(db: Database):
    """
    Health check endpoint
    Returns service status and database connectivity
    """
    health_status = {
        "status": "healthy",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "version": settings.VERSION,
        "service": settings.SERVICE_NAME,
        "checks": {}
    }
    
    # Database connectivity check
    try:
        # Test database connection
        db.execute(text("SELECT 1"))
        health_status["checks"]["database"] = {
            "status": "healthy",
            "message": "Database connection successful"
        }
    except Exception as e:
        health_status["status"] = "unhealthy"
        health_status["checks"]["database"] = {
            "status": "unhealthy",
            "message": f"Database connection failed: {str(e)}"
        }
    
    # Database pool info
    try:
        pool = engine.pool
        health_status["checks"]["database_pool"] = {
            "status": "healthy",
            "pool_size": pool.size(),
            "checked_in": pool.checkedin(),
            "checked_out": pool.checkedout(),
            "overflow": pool.overflow()
        }
    except Exception as e:
        health_status["checks"]["database_pool"] = {
            "status": "unknown",
            "message": f"Could not get pool info: {str(e)}"
        }
    
    return health_status


@router.get("/info", response_model=Dict[str, Any])
async def info():
    """
    Service information endpoint
    Returns detailed service information
    """
    return {
        "service": {
            "name": settings.SERVICE_NAME,
            "version": settings.VERSION,
            "description": settings.SERVICE_DESCRIPTION,
            "author": settings.SERVICE_AUTHOR
        },
        "api": {
            "version": "v1",
            "prefix": settings.API_PREFIX,
            "docs_url": "/docs",
            "redoc_url": "/redoc",
            "openapi_url": "/openapi.json"
        },
        "technology": {
            "framework": "FastAPI",
            "database": "PostgreSQL",
            "orm": "SQLAlchemy",
            "authentication": "JWT OAuth2"
        },
        "environment": {
            "debug": getattr(settings, 'DEBUG', False),
            "database_configured": bool(settings.DATABASE_URL),
            "secret_key_configured": bool(settings.SECRET_KEY and len(settings.SECRET_KEY) > 20),
            "environment": getattr(settings, 'ENVIRONMENT', 'development')
        },
        "features": {
            "authentication": True,
            "database_migrations": True,
            "api_documentation": True,
            "cors_enabled": True,
            "dependency_injection": True
        }
    }


@router.get("/health/live", response_model=Dict[str, str])
async def liveness_probe():
    """
    Kubernetes liveness probe
    Simple check if service is running
    """
    return {
        "status": "alive"
    }


@router.get("/health/ready", response_model=Dict[str, Any])
async def readiness_probe(db: Database):
    """
    Kubernetes readiness probe
    Check if service is ready to accept traffic
    """
    try:
        # Test database connection
        db.execute(text("SELECT 1"))
        return {
            "status": "ready",
            "checks": {
                "database": "ready"
            }
        }
    except Exception as e:
        return {
            "status": "not_ready",
            "checks": {
                "database": f"not_ready: {str(e)}"
            }
        }
