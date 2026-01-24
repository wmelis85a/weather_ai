"""
FastAPI application with LangChain agent using Grok models.
"""
import os
from typing import Optional
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from langchain_xai import ChatXAI
from langchain.agents import create_agent
from langchain_core.tools import tool

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="Weather AI Agent",
    description="A FastAPI application using LangChain with Grok models",
    version="1.0.0"
)

# Get XAI API key from environment
XAI_API_KEY = os.getenv("XAI_API_KEY")

# Define request/response models
class AgentRequest(BaseModel):
    query: str
    model: Optional[str] = "grok-beta"

class AgentResponse(BaseModel):
    query: str
    response: str
    model: str

# Define a simple weather tool for the agent
@tool
def get_weather_info(location: str) -> str:
    """Get weather information for a location.
    
    Args:
        location: The name of the location to get weather for.
        
    Returns:
        Weather information for the location.
    """
    # This is a placeholder - in a real app, you'd call a weather API
    return f"The weather in {location} is sunny with a temperature of 72°F."

# Create tools list
tools = [get_weather_info]

def create_weather_agent(model_name: str = "grok-beta"):
    """Create a LangChain agent with the specified Grok model."""
    if not XAI_API_KEY:
        raise ValueError("XAI_API_KEY environment variable is not set")
    
    # Initialize Grok LLM
    llm = ChatXAI(
        api_key=XAI_API_KEY,
        model=model_name,
        temperature=0.7
    )
    
    # Create the agent with system prompt
    system_prompt = """You are a helpful weather assistant. Use the available tools to answer questions about weather.
    Be friendly and informative in your responses."""
    
    agent = create_agent(
        model=llm,
        tools=tools,
        system_prompt=system_prompt
    )
    
    return agent

@app.get("/")
async def root():
    """Root endpoint - health check."""
    return {
        "message": "Weather AI Agent API",
        "status": "running",
        "version": "1.0.0"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    api_key_status = "configured" if XAI_API_KEY else "missing"
    return {
        "status": "healthy",
        "api_key": api_key_status
    }

@app.post("/agent", response_model=AgentResponse)
async def chat_with_agent(request: AgentRequest):
    """
    Chat with the LangChain agent powered by Grok.
    
    Args:
        request: AgentRequest containing the query and optional model name
        
    Returns:
        AgentResponse with the agent's response
    """
    if not XAI_API_KEY:
        raise HTTPException(
            status_code=500,
            detail="XAI_API_KEY is not configured. Please set it in the .env file."
        )
    
    try:
        # Create agent
        agent = create_weather_agent(request.model)
        
        # Run the agent
        result = agent.invoke({"messages": [{"role": "user", "content": request.query}]})
        
        # Extract the response from messages
        response_text = ""
        if "messages" in result:
            for msg in result["messages"]:
                if hasattr(msg, "content") and msg.content:
                    response_text = msg.content
        
        return AgentResponse(
            query=request.query,
            response=response_text or "No response generated",
            model=request.model
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error running agent: {str(e)}"
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
