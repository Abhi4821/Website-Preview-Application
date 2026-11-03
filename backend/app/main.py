import os
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from app.database import engine
from app.models import SavedURL, User  # noqa: F401
from app.routers.auth import router as auth_router
from app.routers.urls import router as urls_router

load_dotenv()

APP_ENV = os.getenv("APP_ENV", "development").lower()
IS_PRODUCTION = APP_ENV == "production"

docs_url = None if IS_PRODUCTION else "/docs"
redoc_url = None if IS_PRODUCTION else "/redoc"
openapi_url = None if IS_PRODUCTION else "/openapi.json"


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Database schema is managed by Alembic.
    yield
    engine.dispose()


app = FastAPI(
    title=os.getenv("APP_NAME", "Website Preview Application"),
    version="1.0.0",
    description="Signup, login, and save website previews.",
    docs_url=docs_url,
    redoc_url=redoc_url,
    openapi_url=openapi_url,
    lifespan=lifespan,
)

origins = [
    origin.strip()
    for origin in os.getenv(
        "FRONTEND_ORIGIN",
        "http://localhost:5173",
    ).split(",")
    if origin.strip()
]

allowed_methods = ["GET", "POST", "DELETE", "OPTIONS"]
allowed_headers = ["Authorization", "Content-Type", "Accept"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=allowed_methods,
    allow_headers=allowed_headers,
)


app.include_router(auth_router)
app.include_router(urls_router)


@app.get("/", tags=["Health"])
def home():
    return {"message": "Website Preview API is running"}


@app.get("/health", tags=["Health"])
def health():
    return {"status": "ok"}


@app.get("/health/db", tags=["Health"])
def database_health():
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        return {"database": "connected"}

    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database is unavailable.",
        )

# import os

# from dotenv import load_dotenv
# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
# from sqlalchemy import text

# from app.database import Base, engine
# from app.models import SavedURL, User  # noqa: F401 - register models
# from app.routers.auth import router as auth_router
# from app.routers.urls import router as urls_router

# load_dotenv()

# app = FastAPI(
#     title=os.getenv("APP_NAME", "Website Preview Application"),
#     version="1.0.0",
#     description="Signup, login, and save website previews.",
# )

# origins = [
#     origin.strip()
#     for origin in os.getenv("FRONTEND_ORIGIN", "http://localhost:5173").split(",")
#     if origin.strip()
# ]
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# app.include_router(auth_router)
# app.include_router(urls_router)


# @app.on_event("startup")
# def startup() -> None:
#     # Convenient for local assignment development. Use Alembic migrations in production.
#     Base.metadata.create_all(bind=engine)


# @app.get("/", tags=["Health"])
# def home():
#     return {"message": "Website Preview API is running", "docs": "/docs"}


# @app.get("/health/db", tags=["Health"])
# def database_health():
#     with engine.connect() as connection:
#         connection.execute(text("SELECT 1"))
#     return {"database": "connected"}
