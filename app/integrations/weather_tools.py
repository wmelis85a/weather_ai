"""
Weather tools for LangChain agents.
Provides weather information functionality.
"""
from langchain_core.tools import tool


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


def get_tools() -> list:
    """Get list of all available tools for the agent."""
    return [get_weather_info]
