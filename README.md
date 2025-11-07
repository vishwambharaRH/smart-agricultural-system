# Smart Agricultural System Using Raspberry Pi and Arduino Uno

This project is a **smart agricultural IoT system** that monitors **temperature**, **humidity**, **soil moisture**, and **ambient light**, and allows **manual or automated water pump control** through a web interface hosted on a **Raspberry Pi**.

The system uses:
- **Arduino Uno** for analog sensor reading
- **Raspberry Pi (RPi 2B, 32-bit)** for computation & server hosting
- **FastAPI** dashboard for visualization and pump control

---

## Components Used

| Component | Quantity | Purpose |
|----------|----------|---------|
| Raspberry Pi 2B (32-bit) | 1 | Hosts server + controls pump via GPIO |
| Arduino Uno | 1 | Reads analog sensors & sends data to RPi |
| **DHT11** Temperature + Humidity Sensor | 1 | Measures environment temperature/humidity |
| Soil Moisture Sensor | 1 | Measures soil wetness level |
| LDR (Light Dependent Resistor) + 10k Resistor | 1 | Measures ambient light |
| Relay Module (5V, 1-channel)** | 1 | Controls the water pump safely |
| Submersible Water Pump (5V/9V/12V depending on model)** | 1 | Provides irrigation |
| Jumper Wires | — | Signal & power connections |
| External Power Supply for Pump | 1 | Pump should **NOT** be powered from Pi/Arduino |

> **Note:** Make sure the pump and relay share **common ground** with Arduino/RPi.

---

## Wiring Details

### 1) **Sensors → Arduino Uno**

| Sensor | Arduino Pin | Notes |
|-------|-------------|-------|
| **DHT11 Data** | D2 | Use a **10k pull-up** resistor between Data and **5V** |
| Soil Sensor Analog Output | A0 | GND → GND, VCC → 5V |
| LDR Voltage Divider Output | A1 | See diagram below |

#### LDR Voltage Divider
5V --- [LDR] ----┐
├---- A1 → Arduino
GND ---[10kΩ] ---┘

---

### 2) **Arduino → Raspberry Pi (Data Connection)**

| Arduino | Raspberry Pi |
|--------|--------------|
| USB Cable | USB Port on RPi |

The Pi reads sensor values via **Serial** (`/dev/ttyACM0`).

---

### 3) **Pump & Relay Wiring (Critical Safety)**
(Raspberry Pi GPIO17) ----> IN (Relay Module)
(Raspberry Pi GND) ------> GND (Relay Module)
Relay COM ----> Pump + (positive)
Relay NO ----> External Power Supply +
Pump - (negative) ----> External Power Supply -
Raspberry Pi and Pump Power Supply Grounds MUST be connected together.

> **Never power the pump directly from Raspberry Pi or Arduino 5V pins**.  
> Use a separate adapter / battery for the pump.

---

## System Architecture Overview
[ Sensors ]
↓ (Analog + Digital)
[ Arduino ] -- USB Serial --> [ Raspberry Pi ]
↓
FastAPI Dashboard + Logging
↓
GPIO → Relay → Pump

---

## Software Overview

| Component | Language/Library | Role |
|----------|------------------|------|
| Arduino Firmware | C++ / Arduino Core | Reads sensors, outputs JSON over serial |
| Raspberry Pi Server | Python (FastAPI, PySerial, RPi.GPIO) | Hosts API + Dashboard UI |
| Frontend UI | HTML + JavaScript + Chart.js | Displays graphs + manual controls |
| Logging | CSV | Stores historical sensor data every 10 minutes |

---

## 📊 Dashboard & Data Logging

- Visit dashboard in browser:
http://<raspberry-pi-ip>:8000/
- Displays:
- Live and historical temperature & soil moisture graphs
- Pump **ON/OFF** control buttons
- Historical data stored in:
sensor_log.csv

---

## Running the System

### Start the FastAPI Server on Raspberry Pi:
```bash
uvicorn server:app --host 0.0.0.0 --port 8000
Access From Laptop:
http://<pi-local-ip>:8000/
