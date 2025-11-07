#include <DHT.h>

#define DHTPIN 2
#define DHTTYPE DHT22
DHT dht(DHTPIN, DHTTYPE);

const int SOIL_PIN = A0;
const int LDR_PIN = A1;

void setup() {
  Serial.begin(9600);
  dht.begin();
}

void loop() {
  float humidity = dht.readHumidity();
  float temperature = dht.readTemperature();
  int soil = analogRead(SOIL_PIN);
  int light = analogRead(LDR_PIN);

  Serial.print("{\"temp\":");
  Serial.print(temperature);
  Serial.print(",\"hum\":");
  Serial.print(humidity);
  Serial.print(",\"soil\":");
  Serial.print(soil);
  Serial.print(",\"light\":");
  Serial.println(light);
  Serial.println("}");

  delay(2000);
}
