from fastapi import Depends, FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from starlette.exceptions import HTTPException

from .src.core.config import ALLOWED_HOSTS, API_PREFIX
from .src.core.database import Base, SessionLocal, engine
from .src.core.security import get_token_header
from .src.internal import admin
from .src.api.v1.router import api_router

###
# Main application file
###


def get_application() -> FastAPI:
    """Configure, start and return the application"""

    ## Start FastApi App
    application = FastAPI()

    ## Generate database tables
    Base.metadata.create_all(bind=engine)

    ## Mapping api routes
    application.include_router(api_router, prefix=API_PREFIX + "/v1")

    ## Allow cors
    application.add_middleware(
        CORSMiddleware,
        allow_origins=ALLOWED_HOSTS or ["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    ## Example of admin route
    application.include_router(
        admin.router,
        prefix="/admin",
        tags=["admin"],
        dependencies=[Depends(get_token_header)],
        responses={418: {"description": "I'm a teapot"}},
    )

    return application


app = get_application()


@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    """
    The middleware we'll add (just a function) will create
    a new SQLAlchemy SessionLocal for each request, add it to
    the request and then close it once the request is finished.
    """
    response = Response("Internal server error", status_code=500)
    try:
        request.state.db = SessionLocal()
        response = await call_next(request)
    finally:
        request.state.db.close()
    return response
