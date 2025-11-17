from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # Server Configuration
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG: bool = True
    
    # Arduino Configuration
    SERIAL_PORT: str = "/dev/ttyACM0"
    BAUD_RATE: int = 9600
    SERIAL_TIMEOUT: int = 1
    
    # GPIO Configuration
    PUMP_PIN: int = 17
    GPIO_MODE: str = "BCM"  # BCM or BOARD
    
    # Data Logging
    LOG_INTERVAL: int = 5  # seconds (10 minutes)
    LOG_FILE: str = "data/sensor_log.csv"
    MAX_HISTORY_RECORDS: int = 1000
    
    # Sensor Thresholds (for automation)
    SOIL_DRY_THRESHOLD: int = 300  # Below this = dry soil
    SOIL_WET_THRESHOLD: int = 700  # Above this = wet soil
    TEMP_HIGH_THRESHOLD: float = 35.0  # Celsius
    TEMP_LOW_THRESHOLD: float = 10.0   # Celsius
    
    # Auto-watering settings
    AUTO_WATER_ENABLED: bool = False
    AUTO_WATER_DURATION: int = 30  # seconds
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
