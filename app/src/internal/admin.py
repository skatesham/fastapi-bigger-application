from fastapi import APIRouter
from ...resources.strings import ADMIN_SUCCESS_MESSAGE

router = APIRouter()


@router.post("/")
async def update_admin():
    """Example route"""
    return {"message": ADMIN_SUCCESS_MESSAGE}
