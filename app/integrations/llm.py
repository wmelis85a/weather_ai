"""
LLM integration module for XAI Grok models.
Handles initialization and configuration of the language model.
"""
from typing import Optional
from langchain_xai import ChatXAI


def initialize_llm(api_key: str, model_name: str = "grok-beta", temperature: float = 0.7) -> ChatXAI:
    """Initialize and return a ChatXAI LLM instance.
    
    Args:
        api_key: XAI API key
        model_name: Name of the Grok model to use
        temperature: Model temperature (0.0-1.0)
        
    Returns:
        Initialized ChatXAI instance
        
    Raises:
        ValueError: If API key is not provided
    """
    if not api_key:
        raise ValueError("XAI_API_KEY is required but not provided")
    
    return ChatXAI(
        api_key=api_key,
        model=model_name,
        temperature=temperature
    )
