"""
Main API Router for v1 endpoints
Following FastAPI best practices for API organization
"""

from fastapi import APIRouter

from .endpoints import auth, users, cars, stocks, sellers, buyers, sales, health
from app.src.core.config import settings

# Create main API router
api_router = APIRouter()

# Root endpoint
@api_router.get("/", tags=["root"])
async def api_root():
    """API root endpoint - redirects to info"""
    return {
        "message": f"{settings.SERVICE_NAME} API",
        "version": settings.VERSION,
        "docs": "/docs",
        "info": "/system/info",
        "health": "/system/health"
    }

# Include all endpoint routers
api_router.include_router(auth.router, tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(cars.router, prefix="/cars", tags=["cars"])
api_router.include_router(stocks.router, prefix="/stocks", tags=["stocks"])
api_router.include_router(sellers.router, prefix="/sellers", tags=["sellers"])
api_router.include_router(buyers.router, prefix="/buyers", tags=["buyers"])
api_router.include_router(sales.router, prefix="/sales", tags=["sales"])
api_router.include_router(health.router, prefix="/system", tags=["system"])
