/*
 * Configuration file for Arduino sensors
 * Place this file in the same folder as smart_agriculture.ino
 */

#ifndef CONFIG_H
#define CONFIG_H

// ===== SENSOR PIN CONFIGURATION =====
#define DHTPIN 2           // DHT sensor data pin
#define SOIL_PIN A0        // Soil moisture analog pin
#define LDR_PIN A1         // LDR (light sensor) analog pin

// ===== DHT SENSOR TYPE =====
// Uncomment the sensor you're using
#define DHTTYPE DHT22      // DHT22 (AM2302)
// #define DHTTYPE DHT11   // DHT11

// ===== COMMUNICATION SETTINGS =====
#define BAUD_RATE 9600     // Serial baud rate
#define READ_INTERVAL 2000 // Sensor reading interval (ms)
#define NUM_SAMPLES 5      // Number of samples for averaging

// ===== SENSOR CALIBRATION =====
// Soil Moisture Calibration
// Measure these values with your specific sensor
#define SOIL_DRY_VALUE 850    // Sensor value in dry air
#define SOIL_WET_VALUE 400    // Sensor value in water

// LDR Calibration
#define LDR_DARK_VALUE 50     // Sensor value in darkness
#define LDR_BRIGHT_VALUE 900  // Sensor value in bright light

// ===== OPTIONAL FEATURES =====
#define ENABLE_CALIBRATION true  // Send calibrated percentage values
#define ENABLE_DEBUG false        // Enable debug messages
#define ENABLE_LED_INDICATOR false // Use built-in LED for activity

// Built-in LED pin (most Arduinos use pin 13)
#define LED_PIN 13

// ===== SENSOR LIMITS =====
// Temperature thresholds (for validation)
#define TEMP_MIN -40.0
#define TEMP_MAX 80.0

// Humidity thresholds
#define HUM_MIN 0.0
#define HUM_MAX 100.0

#endif