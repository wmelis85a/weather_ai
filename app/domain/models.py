"""
Domain models for Weather AI application.
"""
from typing import List, Optional
from pydantic import BaseModel, Field


class AgentRequest(BaseModel):
    """Request model for agent queries."""
    query: str
    model: Optional[str] = "grok-beta"


class AgentResponse(BaseModel):
    """Response model for agent queries."""
    query: str
    response: str
    model: str


class HealthCheck(BaseModel):
    """Health check response model."""
    status: str
    api_key: str


class WeatherAlert(BaseModel):
    id: int | str

    start_date: Optional[str] = Field(None, alias="data_inicio")
    end_date: Optional[str] = Field(None, alias="data_fim")
    start_time: Optional[str] = Field(None, alias="hora_inicio")
    end_time: Optional[str] = Field(None, alias="hora_fim")

    region: Optional[str] = Field(None, alias="mesorregioes")  # Mudou para plural
    description: Optional[str] = Field(None, alias="descricao")
    severity: Optional[str] = Field(None, alias="severidade")

    risk: List[str] = Field(default_factory=list, alias="riscos")  # Mudou para plural
    instructions: List[str] = Field(default_factory=list, alias="instrucoes")

    class Config:
        populate_by_name = True
        extra = "ignore"

class WeatherAlertResponse(BaseModel):
    hoje: List[WeatherAlert] = Field(default_factory=list)
    futuro: List[WeatherAlert] = Field(default_factory=list)

    class Config:
        extra = "ignore"