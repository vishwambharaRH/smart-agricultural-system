import serial
import json
import logging
from typing import Optional, Dict
from config.settings import settings

logger = logging.getLogger(__name__)

class ArduinoReader:
    """Handles serial communication with Arduino"""
    
    def __init__(self):
        self.ser: Optional[serial.Serial] = None
        self.connect()
    
    def connect(self) -> bool:
        """Establish serial connection to Arduino"""
        try:
            self.ser = serial.Serial(
                settings.SERIAL_PORT,
                settings.BAUD_RATE,
                timeout=settings.SERIAL_TIMEOUT
            )
            logger.info(f"Connected to Arduino on {settings.SERIAL_PORT}")
            return True
        except serial.SerialException as e:
            logger.error(f"Failed to connect to Arduino: {e}")
            return False
    
    def read_sensor_data(self) -> Optional[Dict]:
        """
        Read and parse JSON sensor data from Arduino
        Returns dict with keys: temp, hum, soil, light
        """
        if not self.ser or not self.ser.is_open:
            logger.warning("Serial connection not open")
            return None
        
        try:
            line = self.ser.readline().decode('utf-8').strip()
            
            # Look for JSON data
            if line.startswith("{") and line.endswith("}"):
                data = json.loads(line)
                
                # Validate data structure
                required_keys = ["temp", "hum", "soil", "light"]
                if all(key in data for key in required_keys):
                    return data
                else:
                    logger.warning(f"Incomplete data received: {data}")
                    
        except json.JSONDecodeError as e:
            logger.error(f"JSON parsing error: {e}")
        except UnicodeDecodeError as e:
            logger.error(f"Unicode decode error: {e}")
        except Exception as e:
            logger.error(f"Error reading from Arduino: {e}")
        
        return None
    
    def close(self):
        """Close serial connection"""
        if self.ser and self.ser.is_open:
            self.ser.close()
            logger.info("Arduino connection closed")
    
    def __del__(self):
        self.close()