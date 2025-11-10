import RPi.GPIO as GPIO
import logging
import time
from threading import Timer
from config.settings import settings

logger = logging.getLogger(__name__)

class PumpController:
    """Controls water pump via GPIO relay"""
    
    def __init__(self):
        self.is_on = False
        self.auto_timer: Optional[Timer] = None
        self.setup_gpio()
    
    def setup_gpio(self):
        """Initialize GPIO for pump control"""
        try:
            if settings.GPIO_MODE == "BCM":
                GPIO.setmode(GPIO.BCM)
            else:
                GPIO.setmode(GPIO.BOARD)
            
            GPIO.setup(settings.PUMP_PIN, GPIO.OUT)
            GPIO.output(settings.PUMP_PIN, GPIO.LOW)
            self.is_on = False
            logger.info(f"GPIO initialized - Pump on pin {settings.PUMP_PIN}")
        except Exception as e:
            logger.error(f"GPIO setup failed: {e}")
    
    def turn_on(self) -> bool:
        """Turn pump ON"""
        try:
            GPIO.output(settings.PUMP_PIN, GPIO.HIGH)
            self.is_on = True
            logger.info("Pump turned ON")
            return True
        except Exception as e:
            logger.error(f"Failed to turn pump ON: {e}")
            return False
    
    def turn_off(self) -> bool:
        """Turn pump OFF"""
        try:
            GPIO.output(settings.PUMP_PIN, GPIO.LOW)
            self.is_on = False
            logger.info("Pump turned OFF")
            
            # Cancel any auto-off timer
            if self.auto_timer:
                self.auto_timer.cancel()
                self.auto_timer = None
            
            return True
        except Exception as e:
            logger.error(f"Failed to turn pump OFF: {e}")
            return False
    
    def turn_on_for_duration(self, seconds: int):
        """Turn pump on for specified duration, then auto-off"""
        if self.turn_on():
            self.auto_timer = Timer(seconds, self.turn_off)
            self.auto_timer.start()
            logger.info(f"Pump will auto-off in {seconds} seconds")
    
    def get_status(self) -> dict:
        """Get current pump status"""
        return {
            "is_on": self.is_on,
            "pin": settings.PUMP_PIN
        }
    
    def cleanup(self):
        """Clean up GPIO on shutdown"""
        self.turn_off()
        GPIO.cleanup()
        logger.info("GPIO cleanup completed")
    
    def __del__(self):
        self.cleanup()