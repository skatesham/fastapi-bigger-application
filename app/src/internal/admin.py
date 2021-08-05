from fastapi import APIRouter

router = APIRouter()


@router.post("/")
async def update_admin():
    ''' Example route '''
    return {"message": "Admin getting schwifty"}
