"""
Google Gemini AI integration module.
Handles communication with Google's Generative AI API.
"""
from google import genai


async def generate_with_gemini(prompt: str, model: str = "gemini-3-flash-preview") -> str:
    """
    Generate content using Google's Gemini API.
    
    The client automatically reads the API key from the GEMINI_API_KEY environment variable.
    
    Args:
        prompt: The prompt to send to Gemini
        model: The Gemini model to use (default: gemini-3-flash-preview)
        
    Returns:
        The generated text response from Gemini
        
    Raises:
        Exception: If the API call fails or GEMINI_API_KEY is not set
    """
    try:
        client = genai.Client()
        
        response = client.models.generate_content(
            model=model,
            contents=prompt
        )
        
        return response.text
    except Exception as e:
        raise Exception(f"Gemini API error: {str(e)}")
