"""
FastAPI application with LangChain agent using Grok models.
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.api.routes import router
from app.core.config import settings
from app.scheduler import start_scheduler, scheduler


@asynccontextmanager
async def lifespan(app: FastAPI):
    start_scheduler()
    yield
    scheduler.shutdown()


# Initialize FastAPI app
app = FastAPI(
    lifespan=lifespan,
)

# Include API routes
app.include_router(router)


@app.get("/")
async def root():
    """Root endpoint - application info."""
    return {
        "message": "Weather AI Agent API",
        "status": "running",
        "version": settings.API_VERSION
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host=settings.HOST,
        port=settings.PORT
    )
