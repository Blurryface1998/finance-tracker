"""Create and configure the FastAPI application for the finance tracker backend."""

from fastapi import FastAPI

from app.core.database import Base, engine
from app.core.exceptions.base import AppException
from app.core.exceptions.exception_handlers import app_exception_handler
from app.routes import router

app = FastAPI()
Base.metadata.create_all(bind=engine)
app.include_router(router)
app.add_exception_handler(AppException, app_exception_handler)
