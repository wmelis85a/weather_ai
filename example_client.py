#!/usr/bin/env python
"""
Example script demonstrating how to use the Weather AI Agent API.

This script shows how to:
1. Test the health endpoint
2. Send queries to the agent
3. Handle responses

Prerequisites:
- The FastAPI server must be running (python main.py)
- XAI_API_KEY must be configured in .env file
"""

import requests
import json

# API base URL
BASE_URL = "http://localhost:8000"

def check_health():
    """Check if the API is healthy."""
    response = requests.get(f"{BASE_URL}/health")
    print("Health Check:")
    print(json.dumps(response.json(), indent=2))
    print()

def query_agent(query: str, model: str = "grok-beta"):
    """Send a query to the agent."""
    print(f"Querying agent with: '{query}'")
    print(f"Using model: {model}")
    
    response = requests.post(
        f"{BASE_URL}/agent",
        json={
            "query": query,
            "model": model
        }
    )
    
    if response.status_code == 200:
        result = response.json()
        print("Response:")
        print(f"  Query: {result['query']}")
        print(f"  Model: {result['model']}")
        print(f"  Answer: {result['response']}")
    else:
        print(f"Error: {response.status_code}")
        print(response.json())
    print()

if __name__ == "__main__":
    print("Weather AI Agent - Example Client")
    print("=" * 50)
    print()
    
    # Check health
    try:
        check_health()
    except requests.exceptions.ConnectionError:
        print("Error: Cannot connect to the API. Make sure the server is running.")
        print("Start the server with: python main.py")
        exit(1)
    
    # Example queries
    queries = [
        "What is the weather in New York?",
        "Tell me about the weather in London",
        "What's the temperature in San Francisco?"
    ]
    
    for query in queries:
        try:
            query_agent(query)
        except Exception as e:
            print(f"Error processing query: {e}")
            print()
