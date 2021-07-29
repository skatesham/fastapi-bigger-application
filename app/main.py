from fastapi import Depends, FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware

from .src.dependencies import get_query_token, get_token_header
from .src.internal import admin
from .src.routers.api import router as router_api

from .src.database import engine, SessionLocal, Base
from .src.config import API_PREFIX, ALLOWED_HOSTS


def get_application() -> FastAPI:
    ''' Start and get the application '''
    
    application = FastAPI()

    Base.metadata.create_all(bind=engine)

    application.include_router(router_api, prefix=API_PREFIX)

    application.include_router(
        admin.router,
        prefix="/admin",
        tags=["admin"],
        dependencies=[Depends(get_token_header)],
        responses={418: {"description": "I'm a teapot"}},
    )

    application.add_middleware(
        CORSMiddleware,
        allow_origins=ALLOWED_HOSTS or ["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    return application


app = get_application()


@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    '''
    The middleware we'll add (just a function) will create
    a new SQLAlchemy SessionLocal for each request, add it to
    the request and then close it once the request is finished.
    '''
    response = Response("Internal server error", status_code=500)
    try:
        request.state.db = SessionLocal()
        response = await call_next(request)
    finally:
        request.state.db.close()
    return response

