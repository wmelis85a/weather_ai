"""
API routes for the Weather AI application.
Defines all FastAPI endpoints.
"""
from app.domain.services.nearby_station import fetch_nearby_station_weather
from fastapi import APIRouter, HTTPException
from app.domain.models import AgentRequest, AgentResponse, WeatherAlertResponse, GeminiRequest, GeminiResponse
from app.agents.weather_agent import WeatherAgent
from app.core.config import settings
from app.domain.services.alerts import fetch_active_alerts
from app.integrations.gemini import generate_with_gemini
import json

router = APIRouter()


@router.get("/health" , methods=["GET" , "HEAD"])
async def health_check():
    """Minimal liveness endpoint."""
    return {"status": "ok"}

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
            "model": "gemini-2.5-flash-lite"
        }
        ```
    """
    try:
        alerts_collector = await fetch_active_alerts()
        nearby_station_report = await fetch_nearby_station_weather()
        scheduled_prompt = f"""
        Você é um assistente meteorológico para a Região Metropolitana do Rio de Janeiro.

        ## Dados disponíveis

        ### Alertas ativos:
        {alerts_collector}

        ### Relatório da estação mais próxima:
        {nearby_station_report}

        ## Sua tarefa

        Com base nos dados acima, responda ao usuário em **português brasileiro** seguindo este formato:

        1. **Saudação** – cumprimente de forma natural e breve
        2. **Situação atual** – resuma as condições do momento (temperatura, céu, vento)
        3. **Alertas** – se houver alertas ativos, destaque-os com clareza; se não houver, confirme isso de forma tranquilizadora
        4. **Recomendação** – uma dica prática e objetiva com base nas condições

        Seja direto, informativo e evite linguagem técnica desnecessária.

        ---

        Mensagem do usuário: {request.prompt}
        """

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
