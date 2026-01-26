"""
FastAPI application with LangChain agent using Grok models.
"""
from fastapi import FastAPI
from app.api.routes import router
from app.core.config import settings

# Initialize FastAPI app
app = FastAPI(
    title=settings.API_TITLE,
    description=settings.API_DESCRIPTION,
    version=settings.API_VERSION
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
