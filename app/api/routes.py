"""
API routes for the Weather AI application.
Defines all FastAPI endpoints.
"""
from fastapi import APIRouter, HTTPException
from app.domain.models import AgentRequest, AgentResponse, HealthCheck, WeatherAlertResponse, GeminiRequest, GeminiResponse
from app.agents.weather_agent import WeatherAgent
from app.core.config import settings
from app.domain.services.alerts import fetch_active_alerts
from app.integrations.gemini import generate_with_gemini

router = APIRouter()


@router.get("/health", response_model=HealthCheck)
async def health_check():
    """Health check endpoint."""
    api_key_status = "configured" if settings.XAI_API_KEY else "missing"
    return HealthCheck(
        status="healthy",
        api_key=api_key_status
    )

@router.get("/alerts", response_model=WeatherAlertResponse)
async def get_active_alerts():
    """Get active weather alerts."""
    response = await fetch_active_alerts()
    return response


@router.post("/agent", response_model=AgentResponse)
async def chat_with_agent(request: AgentRequest):
    """
    Chat with the LangChain agent powered by Grok.
    
    Args:
        request: AgentRequest containing the query and optional model name
        
    Returns:
        AgentResponse with the agent's response
    """
    if not settings.XAI_API_KEY:
        raise HTTPException(
            status_code=500,
            detail="XAI_API_KEY is not configured. Please set it in the .env file."
        )
    
    try:
        # Get or create cached agent
        agent = WeatherAgent.get_or_create(settings.XAI_API_KEY, request.model)
        
        # Invoke the agent with the user's query
        response_text = WeatherAgent.invoke(agent, request.query)
        
        return AgentResponse(
            query=request.query,
            response=response_text,
            model=request.model
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error running agent: {str(e)}"
        )


@router.post("/gemini", response_model=GeminiResponse)
async def gemini_endpoint(request: GeminiRequest):
    """
    Generate content using Google's Gemini AI model.
    
    This endpoint sends a prompt to Google's Gemini API and returns the generated response.
    The GEMINI_API_KEY environment variable must be set for this to work.
    
    Args:
        request: GeminiRequest containing the prompt and optional model name
        
    Returns:
        GeminiResponse with the generated text and model information
        
    Example request:
        ```json
        {
            "prompt": "Explain how AI works in a few words",
            "model": "gemini-2.0-flash"
        }
        ```
    """
    try:
        response_text = await generate_with_gemini(request.prompt, request.model)
        
        return GeminiResponse(
            prompt=request.prompt,
            response=response_text,
            model=request.model
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error running Gemini: {str(e)}"
        )
