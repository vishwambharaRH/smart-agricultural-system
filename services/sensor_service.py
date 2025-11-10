import logging
import time
from threading import Thread, Event
from typing import Optional, Dict
from hardware.arduino_reader import ArduinoReader
from hardware.pump_controller import PumpController
from services.data_logger import DataLogger
from config.settings import settings

logger = logging.getLogger(__name__)

class SensorService:
    """Main service coordinating sensors, pump, and logging"""
    
    def __init__(self):
        self.arduino = ArduinoReader()
        self.pump = PumpController()
        self.logger = DataLogger()
        
        self.current_data: Dict = {
            "temp": None,
            "hum": None,
            "soil": None,
            "light": None,
            "timestamp": None
        }
        
        self.running = Event()
        self.log_thread: Optional[Thread] = None
        
    def start_logging_loop(self):
        """Start background thread for periodic data logging"""
        self.running.set()
        self.log_thread = Thread(target=self._logging_loop, daemon=True)
        self.log_thread.start()
        logger.info("Started periodic logging loop")
    
    def _logging_loop(self):
        """Background loop that reads and logs data periodically"""
        while self.running.is_set():
            # Read current sensor data
            data = self.arduino.read_sensor_data()
            
            if data:
                self.current_data = {
                    **data,
                    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
                }
                
                # Log to CSV
                self.logger.log_data(data, self.pump.is_on)
                
                # Check for auto-watering conditions
                if settings.AUTO_WATER_ENABLED:
                    self._check_auto_water(data)
            
            # Wait for next logging interval
            time.sleep(settings.LOG_INTERVAL)
    
    def _check_auto_water(self, data: Dict):
        """Check if auto-watering should trigger"""
        soil = data.get("soil")
        
        if soil is None:
            return
        
        # If soil is dry and pump is not already on
        if soil < settings.SOIL_DRY_THRESHOLD and not self.pump.is_on:
            logger.info(f"Auto-watering triggered (soil: {soil})")
            self.pump.turn_on_for_duration(settings.AUTO_WATER_DURATION)
    
    def get_current_data(self) -> Dict:
        """Get latest sensor readings"""
        # Try to get fresh data
        fresh_data = self.arduino.read_sensor_data()
        if fresh_data:
            self.current_data = {
                **fresh_data,
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
            }
        
        return self.current_data
    
    def get_system_status(self) -> Dict:
        """Get complete system status"""
        return {
            "sensors": self.current_data,
            "pump": self.pump.get_status(),
            "auto_water_enabled": settings.AUTO_WATER_ENABLED,
            "settings": {
                "soil_dry_threshold": settings.SOIL_DRY_THRESHOLD,
                "soil_wet_threshold": settings.SOIL_WET_THRESHOLD,
                "log_interval": settings.LOG_INTERVAL
            }
        }
    
    def stop(self):
        """Stop the service and cleanup"""
        logger.info("Stopping sensor service...")
        self.running.clear()
        
        if self.log_thread:
            self.log_thread.join(timeout=2)
        
        self.pump.cleanup()
        self.arduino.close()
        logger.info("Sensor service stopped")