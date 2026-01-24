# Weather AI

Weather and forecast AI powered advisor using FastAPI and LangChain with Grok models.

## Features

- FastAPI application with RESTful endpoints
- LangChain agent powered by Grok LLM models
- Weather information tool integration
- Simple and extensible architecture

## Prerequisites

- Python 3.8+
- XAI API Key (get one from https://console.x.ai/)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/wmelis85a/weather_ai.git
cd weather_ai
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env and add your XAI_API_KEY
```

## Usage

### Running the Application

Start the FastAPI server:
```bash
python main.py
```

Or use uvicorn directly:
```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

### API Endpoints

#### Health Check
```bash
curl http://localhost:8000/health
```

#### Chat with Agent
```bash
curl -X POST http://localhost:8000/agent \
  -H "Content-Type: application/json" \
  -d '{"query": "What is the weather in New York?"}'
```

#### Interactive API Documentation

Visit `http://localhost:8000/docs` for the interactive Swagger UI documentation.

## Available Grok Models

- `grok-beta` (default)
- `grok-vision-beta`

You can specify the model in your request:
```bash
curl -X POST http://localhost:8000/agent \
  -H "Content-Type: application/json" \
  -d '{"query": "What is the weather in London?", "model": "grok-beta"}'
```

## Project Structure

```
weather_ai/
├── main.py              # FastAPI application with LangChain agent
├── requirements.txt     # Python dependencies
├── .env.example        # Example environment variables
└── README.md           # This file
```

## License

MIT
