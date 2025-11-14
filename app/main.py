"""FastAPI application."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.logging import logger
from app.api.v1 import api_router

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="AWS Service Automation & Control Platform",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(api_router)


@app.on_event("startup")
async def startup_event():
    """Application startup event."""
    logger.info(
        "application_started",
        app_name=settings.APP_NAME,
        version=settings.APP_VERSION,
        environment=settings.ENVIRONMENT,
    )


@app.on_event("shutdown")
async def shutdown_event():
    """Application shutdown event."""
    logger.info("application_shutdown")


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "AWS Automation Platform API",
        "version": settings.APP_VERSION,
        "docs": "/docs",
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}
