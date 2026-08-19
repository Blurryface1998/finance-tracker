"""Create and configure the FastAPI application for the finance tracker backend."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.analytics.routes import router as analytics_router
from app.auth.routes import router as authentication_router
from app.core.exceptions.base import AppException
from app.core.exceptions.exception_handlers import app_exception_handler
from app.core.logging import logger
from app.transactions.routes import router as transaction_router

app = FastAPI(title="Finance Tracker API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logger.info("Initializing Finance Tracker API")
app.add_exception_handler(AppException, app_exception_handler)

app.include_router(authentication_router)
app.include_router(analytics_router)
app.include_router(transaction_router)
logger.info("API routes and exception handlers registered")
