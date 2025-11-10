from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class SensorData(BaseModel):
    """Current sensor readings"""
    temp: Optional[float] = Field(None, description="Temperature in Celsius")
    hum: Optional[float] = Field(None, description="Humidity percentage")
    soil: Optional[int] = Field(None, description="Soil moisture level (0-1023)")
    light: Optional[int] = Field(None, description="Light level (0-1023)")
    timestamp: Optional[str] = Field(None, description="Reading timestamp")

class PumpStatus(BaseModel):
    """Pump status response"""
    is_on: bool
    pin: int

class PumpControl(BaseModel):
    """Pump control request"""
    duration: Optional[int] = Field(None, description="Auto-off duration in seconds")

class SystemStatus(BaseModel):
    """Complete system status"""
    sensors: SensorData
    pump: PumpStatus
    auto_water_enabled: bool
    settings: dict

class HistoricalRecord(BaseModel):
    """Single historical data record"""
    timestamp: str
    temp: str
    humidity: str
    soil_moisture: str
    light_level: str
    pump_status: str

class Response(BaseModel):
    """Generic API response"""
    success: bool
    message: str
    data: Optional[dict] = None