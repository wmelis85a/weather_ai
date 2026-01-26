"""
Weather Agent implementation using LangChain.
Handles agent creation, caching, and invocation.
"""
from typing import Dict, Optional
from langchain.agents import create_agent
from langchain_xai import ChatXAI
from app.integrations.llm import initialize_llm
from app.integrations.weather_tools import get_tools


class WeatherAgent:
    """Weather agent powered by LangChain and Grok."""
    
    # Cache for agents by model name
    _agent_cache: Dict[str, any] = {}
    
    SYSTEM_PROMPT = """You are a helpful weather assistant. Use the available tools to answer questions about weather.
    Be friendly and informative in your responses."""
    
    @staticmethod
    def get_or_create(api_key: str, model_name: str = "grok-beta") -> any:
        """Get or create a cached LangChain agent with the specified Grok model.
        
        Args:
            api_key: XAI API key
            model_name: Name of the Grok model to use
            
        Returns:
            Initialized and cached LangChain agent
            
        Raises:
            ValueError: If API key is not configured
        """
        # Check cache first
        if model_name in WeatherAgent._agent_cache:
            return WeatherAgent._agent_cache[model_name]
        
        if not api_key:
            raise ValueError("XAI_API_KEY environment variable is not set")
        
        # Initialize Grok LLM
        llm = initialize_llm(api_key, model_name)
        
        # Get available tools
        tools = get_tools()
        
        # Create the agent with system prompt
        agent = create_agent(
            model=llm,
            tools=tools,
            system_prompt=WeatherAgent.SYSTEM_PROMPT
        )
        
        # Cache the agent
        WeatherAgent._agent_cache[model_name] = agent
        
        return agent
    
    @staticmethod
    def invoke(agent: any, query: str) -> str:
        """Invoke the agent with a query.
        
        Args:
            agent: The LangChain agent instance
            query: User's query
            
        Returns:
            Agent's response text
        """
        result = agent.invoke({
            "messages": [
                {"role": "user", "content": query}
            ]
        })
        
        # Extract the final response from the agent
        response_text = ""
        if "messages" in result and len(result["messages"]) > 0:
            # Get the last message which should be the agent's response
            last_message = result["messages"][-1]
            if hasattr(last_message, "content"):
                response_text = last_message.content
            elif isinstance(last_message, dict) and "content" in last_message:
                response_text = last_message["content"]
        
        if not response_text:
            response_text = str(result.get("output", "No response generated"))
        
        return response_text
    
    @staticmethod
    def clear_cache() -> None:
        """Clear the agent cache."""
        WeatherAgent._agent_cache.clear()
