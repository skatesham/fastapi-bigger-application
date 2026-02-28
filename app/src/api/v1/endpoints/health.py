from datetime import datetime
from typing import Dict, Any

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text

from ...deps import Database
from ....core.config import settings

router = APIRouter()


@router.get("/health")
async def health_check(db: Database) -> Dict[str, Any]:
    """
    Complete health check endpoint
    Returns service status, database connectivity, and pool information
    """
    health_status = {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "version": settings.VERSION,
        "service": settings.SERVICE_NAME,
        "checks": {}
    }
    
    # Database connectivity check
    try:
        # Test database connection
        result = db.execute(text("SELECT 1"))
        if result.fetchone():
            health_status["checks"]["database"] = {
                "status": "healthy",
                "message": "Database connection successful"
            }
        else:
            health_status["checks"]["database"] = {
                "status": "unhealthy",
                "message": "Database connection failed"
            }
            health_status["status"] = "unhealthy"
    except Exception as e:
        health_status["checks"]["database"] = {
            "status": "unhealthy",
            "message": f"Database error: {str(e)}"
        }
        health_status["status"] = "unhealthy"
    
    # Database pool check
    try:
        pool = db.get_bind().pool
        if pool:
            health_status["checks"]["database_pool"] = {
                "status": "healthy",
                "pool_size": pool.size(),
                "checked_in": pool.checkedin(),
                "checked_out": pool.checkedout(),
                "overflow": pool.overflow()
            }
        else:
            health_status["checks"]["database_pool"] = {
                "status": "unknown",
                "message": "Pool information not available"
            }
    except Exception as e:
        health_status["checks"]["database_pool"] = {
            "status": "unknown",
            "message": f"Pool check error: {str(e)}"
        }
    
    return health_status


@router.get("/health/live")
async def liveness_probe() -> Dict[str, Any]:
    """
    Kubernetes liveness probe
    Simple alive check - returns 200 if service is running
    """
    return {
        "status": "alive",
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }


@router.get("/health/ready")
async def readiness_probe(db: Database) -> Dict[str, Any]:
    """
    Kubernetes readiness probe
    Checks if service is ready to accept traffic
    """
    try:
        # Test database connection
        result = db.execute(text("SELECT 1"))
        if result.fetchone():
            return {
                "status": "ready",
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "checks": {
                    "database": {
                        "status": "healthy",
                        "message": "Database connection successful"
                    }
                }
            }
        else:
            return {
                "status": "not_ready",
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "checks": {
                    "database": {
                        "status": "unhealthy",
                        "message": "Database connection failed"
                    }
                }
            }
    except Exception as e:
        return {
            "status": "not_ready",
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "checks": {
                "database": {
                    "status": "unhealthy",
                    "message": f"Database error: {str(e)}"
                }
            }
        }


@router.get("/info")
async def service_info() -> Dict[str, Any]:
    """
    Service information endpoint
    Returns detailed service information and configuration
    """
    return {
        "service": {
            "name": settings.SERVICE_NAME,
            "version": settings.VERSION,
            "description": settings.SERVICE_DESCRIPTION,
            "author": settings.SERVICE_AUTHOR
        },
        "technology": {
            "framework": "FastAPI",
            "database": "PostgreSQL",
            "orm": "SQLAlchemy",
            "authentication": "JWT OAuth2"
        },
        "environment": {
            "debug": settings.DEBUG,
            "database_configured": bool(settings.DATABASE_URL),
            "secret_key_configured": bool(settings.SECRET_KEY),
            "environment": settings.ENVIRONMENT
        }
    }


@router.get("/")
async def api_root() -> Dict[str, Any]:
    """
    API root endpoint
    Returns basic API information and available endpoints
    """
    return {
        "name": settings.SERVICE_NAME,
        "version": settings.VERSION,
        "description": "FastAPI Car Shop ERP API",
        "endpoints": {
            "health": "/api/v1/system/health",
            "info": "/api/v1/system/info",
            "auth": "/api/v1/auth/",
            "buyers": "/api/v1/buyers/",
            "cars": "/api/v1/cars/",
            "sellers": "/api/v1/sellers/",
            "stocks": "/api/v1/stocks/",
            "sales": "/api/v1/sales/"
        },
        "documentation": {
            "swagger": "/docs",
            "redoc": "/redoc"
        }
    }
