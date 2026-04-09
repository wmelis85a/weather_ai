"""
Domain models for Weather AI application.
"""
from typing import List, Optional ,Any
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
        pass

class NearbyStationWeatherData(BaseModel):
    name: str = Field(alias="NOME")

    class Config:
        populate_by_name = True
        extra = "ignore"

class NearbyStationWeatherReport(BaseModel):
    low: Any = Field(alias="TEM_MIN")
    high: Any = Field(alias="TEM_MAX")
    current: Any = Field(alias="TEM_INS")
    rainfall: Any = Field(alias="CHUVA")
    wind_speed: Any = Field(alias="VEN_VEL")
    wind_burst: Any = Field(alias="VEN_RAJ")
    measured_at: Any = Field(alias="HR_MEDICAO")

    class Config:
        populate_by_name = True
        extra = "ignore"

class NearbyStationWeatherResponse(BaseModel):
    station: NearbyStationWeatherData = Field(alias="estacao")
    report: NearbyStationWeatherReport = Field(alias="dados")

    class Config:
        populate_by_name = True
        extra = "ignore"


class GeminiRequest(BaseModel):
    """Request model for Gemini generation."""
    prompt: Optional[str] = Field(..., description="The prompt to send to Gemini")
    model: Optional[str] = Field("gemini-2.5-flash-lite", description="The Gemini model to use")


class GeminiResponse(BaseModel):
    """Response model for Gemini generation."""
    prompt: str
    response: str
    model: str

    class Config:
        extra = "ignore"