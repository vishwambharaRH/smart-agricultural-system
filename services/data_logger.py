import csv
import os
import logging
from datetime import datetime
from typing import Dict, List
from threading import Lock
from config.settings import settings

logger = logging.getLogger(__name__)

class DataLogger:
    """Handles CSV logging of sensor data"""
    
    def __init__(self):
        self.log_file = settings.LOG_FILE
        self.lock = Lock()
        self._ensure_file_exists()
    
    def _ensure_file_exists(self):
        """Create CSV file with headers if it doesn't exist"""
        os.makedirs(os.path.dirname(self.log_file), exist_ok=True)
        
        if not os.path.isfile(self.log_file):
            with open(self.log_file, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([
                    "timestamp", 
                    "temp", 
                    "humidity", 
                    "soil_moisture", 
                    "light_level",
                    "pump_status"
                ])
            logger.info(f"Created log file: {self.log_file}")
    
    def log_data(self, sensor_data: Dict, pump_status: bool = False):
        """
        Append sensor data to CSV log
        
        Args:
            sensor_data: Dict with temp, hum, soil, light
            pump_status: Current pump on/off state
        """
        with self.lock:
            try:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                row = [
                    timestamp,
                    sensor_data.get("temp", ""),
                    sensor_data.get("hum", ""),
                    sensor_data.get("soil", ""),
                    sensor_data.get("light", ""),
                    "ON" if pump_status else "OFF"
                ]
                
                with open(self.log_file, 'a', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow(row)
                
                logger.debug(f"Data logged: {row}")
                
            except Exception as e:
                logger.error(f"Failed to log data: {e}")
    
    def get_history(self, limit: int = None) -> List[Dict]:
        """
        Read historical data from CSV
        
        Args:
            limit: Maximum number of records to return (most recent)
        
        Returns:
            List of dictionaries containing sensor readings
        """
        if not os.path.isfile(self.log_file):
            return []
        
        data = []
        try:
            with open(self.log_file, 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    data.append(row)
            
            # Return most recent records
            if limit:
                data = data[-limit:]
            
            logger.debug(f"Retrieved {len(data)} historical records")
            return data
            
        except Exception as e:
            logger.error(f"Failed to read history: {e}")
            return []
    
    def get_summary_stats(self) -> Dict:
        """Calculate summary statistics from historical data"""
        history = self.get_history()
        
        if not history:
            return {}
        
        try:
            temps = [float(r["temp"]) for r in history if r["temp"]]
            soils = [int(r["soil_moisture"]) for r in history if r["soil_moisture"]]
            
            return {
                "total_records": len(history),
                "avg_temperature": sum(temps) / len(temps) if temps else 0,
                "avg_soil_moisture": sum(soils) / len(soils) if soils else 0,
                "min_temperature": min(temps) if temps else 0,
                "max_temperature": max(temps) if temps else 0,
            }
        except Exception as e:
            logger.error(f"Failed to calculate stats: {e}")
            return {}
    
    def clear_old_logs(self, keep_last_n: int = 10000):
        """Keep only the most recent N records"""
        history = self.get_history()
        
        if len(history) <= keep_last_n:
            return
        
        with self.lock:
            try:
                # Keep only recent records
                recent = history[-keep_last_n:]
                
                with open(self.log_file, 'w', newline='') as f:
                    if recent:
                        writer = csv.DictWriter(f, fieldnames=recent[0].keys())
                        writer.writeheader()
                        writer.writerows(recent)
                
                logger.info(f"Cleared old logs, kept {len(recent)} records")
            except Exception as e:
                logger.error(f"Failed to clear old logs: {e}")