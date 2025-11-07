from fastapi import FastAPI
from fastapi.responses import JSONResponse, HTMLResponse
import serial, json, csv, os, time, threading
import RPi.GPIO as GPIO

# --- SERIAL CONNECTION ---
ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)

# --- PUMP CONTROL SETUP ---
PUMP_PIN = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(PUMP_PIN, GPIO.OUT)
GPIO.output(PUMP_PIN, GPIO.LOW)

app = FastAPI()
current_data = {"temp": None, "hum": None, "soil": None, "light": None}

# --- READ FROM ARDUINO ---
def read_from_arduino():
    global current_data
    try:
        line = ser.readline().decode().strip()
        if line.startswith("{") and line.endswith("}"):
            current_data = json.loads(line)
    except:
        pass

# --- DATA LOGGING TO CSV EVERY 10 MINUTES ---
def log_data_periodically():
    filename = "sensor_log.csv"
    file_exists = os.path.isfile(filename)

    with open(filename, "a", newline="") as csvfile:
        writer = csv.writer(csvfile)
        if not file_exists:
            writer.writerow(["timestamp", "temp", "hum", "soil", "light"])

        while True:
            read_from_arduino()
            row = [
                time.strftime("%Y-%m-%d %H:%M:%S"),
                current_data["temp"],
                current_data["hum"],
                current_data["soil"],
                current_data["light"]
            ]
            writer.writerow(row)
            csvfile.flush()
            time.sleep(600)  # 600 seconds = 10 minutes

# Start logging thread
threading.Thread(target=log_data_periodically, daemon=True).start()

# --- API ROUTES ---
@app.get("/data")
def get_data():
    read_from_arduino()
    return current_data

@app.post("/pump/on")
def pump_on():
    GPIO.output(PUMP_PIN, GPIO.HIGH)
    return JSONResponse({"pump": "ON"})

@app.post("/pump/off")
def pump_off():
    GPIO.output(PUMP_PIN, GPIO.LOW)
    return JSONResponse({"pump": "OFF"})

@app.get("/history")
def get_history(limit: int = 300):
    if not os.path.isfile("sensor_log.csv"):
        return []
    data = []
    with open("sensor_log.csv") as f:
        reader = csv.DictReader(f)
        for row in reader:
            data.append(row)
    return data[-limit:]

# --- DASHBOARD UI ---
@app.get("/", response_class=HTMLResponse)
def dashboard():
    return """
<!DOCTYPE html>
<html>
<head>
  <title>Smart Agriculture Dashboard</title>
  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
</head>
<body style="font-family: sans-serif; margin: 40px;">
  <h1>🌱 Smart Agriculture Control Panel</h1>

  <button onclick="fetch('/pump/on', {method:'POST'})">Pump ON</button>
  <button onclick="fetch('/pump/off', {method:'POST'})">Pump OFF</button>

  <h2>Historical Data</h2>
  <canvas id="chart" width="600" height="300"></canvas>

  <script>
    async function loadData() {
      const response = await fetch('/history');
      const data = await response.json();

      const labels = data.map(d => d.timestamp);
      const temps = data.map(d => parseFloat(d.temp));
      const soils = data.map(d => parseInt(d.soil));

      const ctx = document.getElementById('chart').getContext('2d');
      new Chart(ctx, {
        type: 'line',
        data: {
          labels: labels,
          datasets: [
            { label: 'Temperature (°C)', data: temps, borderWidth: 2 },
            { label: 'Soil Moisture', data: soils, borderWidth: 2 }
          ]
        }
      });
    }
    loadData();
  </script>
</body>
</html>
"""
