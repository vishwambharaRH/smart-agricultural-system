/*
 * Smart Agriculture System - Arduino Uno
 * 
 * Reads sensors and sends JSON data via Serial to Raspberry Pi
 * 
 * Sensors:
 * - DHT22: Temperature & Humidity (Pin D2)
 * - Soil Moisture: Analog (Pin A0)
 * - LDR: Light sensor (Pin A1)
 */

#include <DHT.h>

// ===== PIN DEFINITIONS =====
#define DHTPIN 2           // DHT22 data pin
#define DHTTYPE DHT11      // DHT sensor type (DHT22 or DHT11)
#define SOIL_PIN A0        // Soil moisture sensor
#define LDR_PIN A1         // Light sensor (LDR)

// ===== CONFIGURATION =====
#define BAUD_RATE 9600     // Serial communication speed
#define READ_INTERVAL 1000// Reading interval in milliseconds
#define NUM_SAMPLES 5      // Number of samples for averaging

// ===== SENSOR OBJECTS =====
DHT dht(DHTPIN, DHTTYPE);

// ===== GLOBAL VARIABLES =====
unsigned long lastReadTime = 0;

// ===== SETUP =====
void setup() {
  // Initialize serial communication
  Serial.begin(BAUD_RATE);
  
  // Initialize DHT sensor
  dht.begin();
  
  // Wait for serial connection
  while (!Serial) {
    delay(10);
  }
  
  // Send startup message
  Serial.println("{\"status\":\"Arduino Ready\"}");
  
  // Small delay to stabilize sensors
  delay(2000);
}

// ===== MAIN LOOP =====
void loop() {
  unsigned long currentTime = millis();
  
  // Read sensors at specified interval
  if (currentTime - lastReadTime >= READ_INTERVAL) {
    lastReadTime = currentTime;
    
    // Read all sensors
    float temperature = readTemperature();
    float humidity = readHumidity();
    int soilMoisture = readSoilMoisture();
    int lightLevel = readLightLevel();
    
    // Send JSON data
    sendSensorData(temperature, humidity, soilMoisture, lightLevel);
  }
}

// ===== SENSOR READING FUNCTIONS =====

/**
 * Read temperature from DHT sensor
 * Returns temperature in Celsius
 */
float readTemperature() {
  float temp = dht.readTemperature();
  
  // Check if reading failed
  if (isnan(temp)) {
    return -999.0; // Error value
  }
  
  return temp;
}

/**
 * Read humidity from DHT sensor
 * Returns humidity percentage
 */
float readHumidity() {
  float hum = dht.readHumidity();
  
  // Check if reading failed
  if (isnan(hum)) {
    return -999.0; // Error value
  }
  
  return hum;
}

/**
 * Read soil moisture sensor
 * Returns averaged analog value (0-1023)
 * Lower value = more moisture
 */
int readSoilMoisture() {
  long sum = 0;
  
  // Take multiple samples and average
  for (int i = 0; i < NUM_SAMPLES; i++) {
    sum += analogRead(SOIL_PIN);
    delay(10);
  }
  
  return sum / NUM_SAMPLES;
}

/**
 * Read light level from LDR
 * Returns averaged analog value (0-1023)
 * Higher value = more light
 */
int readLightLevel() {
  long sum = 0;
  
  // Take multiple samples and average
  for (int i = 0; i < NUM_SAMPLES; i++) {
    sum += analogRead(LDR_PIN);
    delay(10);
  }
  
  return sum / NUM_SAMPLES;
}

// ===== DATA TRANSMISSION =====

/**
 * Send sensor data as JSON via Serial
 */
void sendSensorData(float temp, float hum, int soil, int light) {
  // Build JSON string
  Serial.print("{");
  Serial.print("\"temp\":");
  Serial.print(temp, 2); // 2 decimal places
  Serial.print(",\"hum\":");
  Serial.print(hum, 2);
  Serial.print(",\"soil\":");
  Serial.print(soil);
  Serial.print(",\"light\":");
  Serial.print(light);
  Serial.println("}");
  
  // Flush to ensure data is sent
  Serial.flush();
}

// ===== UTILITY FUNCTIONS =====

/**
 * Map analog value to percentage (optional utility)
 */
int mapToPercentage(int value, int minVal, int maxVal) {
  return map(value, minVal, maxVal, 0, 100);
}