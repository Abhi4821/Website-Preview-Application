import os

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from app.database import Base, engine
from app.models import SavedURL, User  # noqa: F401 - register models
from app.routers.auth import router as auth_router
from app.routers.urls import router as urls_router

load_dotenv()

app = FastAPI(
    title=os.getenv("APP_NAME", "Website Preview Application"),
    version="1.0.0",
    description="Signup, login, and save website previews.",
)

origins = [
    origin.strip()
    for origin in os.getenv("FRONTEND_ORIGIN", "http://localhost:5173").split(",")
    if origin.strip()
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(urls_router)


@app.on_event("startup")
def startup() -> None:
    # Convenient for local assignment development. Use Alembic migrations in production.
    Base.metadata.create_all(bind=engine)


@app.get("/", tags=["Health"])
def home():
    return {"message": "Website Preview API is running", "docs": "/docs"}


@app.get("/health/db", tags=["Health"])
def database_health():
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))
    return {"database": "connected"}
