"""
FastAPI application with LangChain agent using Grok models.
"""
import os
from typing import Optional
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from langchain_xai import ChatXAI
from langchain.agents import AgentExecutor, create_react_agent
from langchain.prompts import PromptTemplate
from langchain_core.tools import Tool

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
def get_weather_info(location: str) -> str:
    """Get weather information for a location."""
    # This is a placeholder - in a real app, you'd call a weather API
    return f"The weather in {location} is sunny with a temperature of 72°F."

# Create tools for the agent
tools = [
    Tool(
        name="WeatherInfo",
        func=get_weather_info,
        description="Useful for getting weather information for a specific location. Input should be a location name."
    )
]

# Define the prompt template for the agent
template = """Answer the following questions as best you can. You have access to the following tools:

{tools}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

Question: {input}
Thought: {agent_scratchpad}"""

prompt = PromptTemplate.from_template(template)

def create_agent_executor(model_name: str = "grok-beta") -> AgentExecutor:
    """Create an agent executor with the specified Grok model."""
    if not XAI_API_KEY:
        raise ValueError("XAI_API_KEY environment variable is not set")
    
    # Initialize Grok LLM
    llm = ChatXAI(
        api_key=XAI_API_KEY,
        model=model_name,
        temperature=0.7
    )
    
    # Create the agent
    agent = create_react_agent(llm, tools, prompt)
    
    # Create agent executor
    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
        handle_parsing_errors=True,
        max_iterations=5
    )
    
    return agent_executor

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
        # Create agent executor
        agent_executor = create_agent_executor(request.model)
        
        # Run the agent
        result = agent_executor.invoke({"input": request.query})
        
        return AgentResponse(
            query=request.query,
            response=result.get("output", "No response generated"),
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
