"""Create and configure the FastAPI application for the finance tracker backend."""

from fastapi import FastAPI

from app.core.database import Base, engine
from app.routes import router

app = FastAPI()
Base.metadata.create_all(bind=engine)
app.include_router(router)
