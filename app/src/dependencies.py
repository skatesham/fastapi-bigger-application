from fastapi import Header, HTTPException

from .database import SessionLocal


def get_db():
    ''' Method for configure database '''
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
    
    
async def get_token_header(x_token: str = Header(...)):
    ''' Exemplo of header validation dependency '''
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")


async def get_query_token(token: str):
    ''' Exemplo of header validation dependency '''
    if token != "jessica":
        raise HTTPException(status_code=400, detail="No Jessica token provided")

