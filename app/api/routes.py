"""
API routes for the Weather AI application.
Defines all FastAPI endpoints.
"""
from app.domain.services.nearby_station import fetch_nearby_station_weather
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
            "model": "gemini-2.0-flash"
        }
        ```
    """
    try:
        alerts_collector = await fetch_active_alerts()
        nearby_station_report = await fetch_nearby_station_weather()
        scheduled_prompt = f"You are a helpful assistant that provides weather information. Here are the current active weather alerts:\n\n{alerts_collector} and {nearby_station_report}\n\nNow, inform the user, in portuguese BR, if there are any active alerts for the Rio de Janeiro metro area. Respond in a friendly way , by greeting the user and informing the news as if in a weather news website\n\n{request.prompt}"

        response_text = await generate_with_gemini(scheduled_prompt, request.model)
        
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
