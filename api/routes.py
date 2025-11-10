from fastapi import APIRouter, HTTPException
from typing import List
from api.models import (
    SensorData, PumpStatus, PumpControl, 
    SystemStatus, HistoricalRecord, Response
)

router = APIRouter()

# This will be injected by main.py
sensor_service = None

def init_routes(service):
    """Initialize routes with sensor service dependency"""
    global sensor_service
    sensor_service = service

@router.get("/api/data", response_model=SensorData)
async def get_current_data():
    """Get current sensor readings"""
    try:
        data = sensor_service.get_current_data()
        return SensorData(**data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/api/status", response_model=SystemStatus)
async def get_system_status():
    """Get complete system status"""
    try:
        status = sensor_service.get_system_status()
        return SystemStatus(**status)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/api/pump/on", response_model=Response)
async def turn_pump_on(control: PumpControl = PumpControl()):
    """Turn pump ON, optionally with auto-off duration"""
    try:
        if control.duration:
            sensor_service.pump.turn_on_for_duration(control.duration)
            message = f"Pump turned ON for {control.duration} seconds"
        else:
            sensor_service.pump.turn_on()
            message = "Pump turned ON"
        
        return Response(
            success=True,
            message=message,
            data={"is_on": sensor_service.pump.is_on}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/api/pump/off", response_model=Response)
async def turn_pump_off():
    """Turn pump OFF"""
    try:
        sensor_service.pump.turn_off()
        return Response(
            success=True,
            message="Pump turned OFF",
            data={"is_on": sensor_service.pump.is_on}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/api/pump/status", response_model=PumpStatus)
async def get_pump_status():
    """Get current pump status"""
    try:
        status = sensor_service.pump.get_status()
        return PumpStatus(**status)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/api/history", response_model=List[HistoricalRecord])
async def get_history(limit: int = 300):
    """Get historical sensor data"""
    try:
        history = sensor_service.logger.get_history(limit=limit)
        return [HistoricalRecord(**record) for record in history]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/api/stats")
async def get_statistics():
    """Get summary statistics"""
    try:
        stats = sensor_service.logger.get_summary_stats()
        return Response(
            success=True,
            message="Statistics retrieved",
            data=stats
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))