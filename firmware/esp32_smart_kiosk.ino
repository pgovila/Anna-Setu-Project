/*
 * =====================================================================================
 * ANNA-SETU: SMART IoT FOOD INTAKE & SEGREGATION STATION (TRACK B FIRMWARE)
 * Platform: ESP32 WROOM-32 Microcontroller
 * Framework: Arduino / C++
 * Target Deployment: Campus Dining Hall Surplus & Plate Waste Station
 * 
 * Circuit Pinout Connections:
 * -------------------------------------------------------------
 * 1. HX711 Load Cell Amplifier (0 - 50 kg Heavy Duty Scale):
 *    - VCC  -> 5V / 3.3V
 *    - GND  -> GND
 *    - DT   -> GPIO 18 (Data)
 *    - SCK  -> GPIO 19 (Clock)
 * 
 * 2. MLX90614 Contactless Infrared Temperature Sensor (I2C):
 *    - VCC  -> 3.3V
 *    - GND  -> GND
 *    - SDA  -> GPIO 21 (I2C SDA)
 *    - SCL  -> GPIO 22 (I2C SCL)
 * 
 * 3. HC-SR04 Ultrasonic Plate Waste Fill Sensor:
 *    - VCC  -> 5V
 *    - GND  -> GND
 *    - TRIG -> GPIO 5
 *    - ECHO -> GPIO 4 (via voltage divider)
 * 
 * 4. User Feedback LEDs & Piezo Buzzer:
 *    - Green LED (Safe)     -> GPIO 12
 *    - Red LED (Rejected)   -> GPIO 14
 *    - Piezo Buzzer         -> GPIO 27
 *    - Solenoid Lock Relay  -> GPIO 26 (Unlocks Green Bio-Compost Bin on reject)
 * =====================================================================================
 */

#include <WiFi.h>
#include <HTTPClient.h>
#include <Wire.h>
#include <ArduinoJson.h>

// --- WiFi Credentials ---
const char* WIFI_SSID     = "CAMPUS_IOT_WIFI";
const char* WIFI_PASSWORD = "CampusSecurePassword";

// --- Anna-Setu Cloud / Local Edge API Endpoint ---
const char* API_ENDPOINT  = "http://192.168.1.100:8000/api/iot/telemetry";
const char* STATION_ID    = "ANNA-SETU-KIOSK-UPES-01";

// --- Pin Definitions ---
const int PIN_HX711_DT   = 18;
const int PIN_HX711_SCK  = 19;
const int PIN_US_TRIG    = 5;
const int PIN_US_ECHO    = 4;
const int PIN_LED_GREEN  = 12;
const int PIN_LED_RED    = 14;
const int PIN_BUZZER     = 27;
const int PIN_RELAY_LOCK = 26;

// --- Calibration Constants ---
const float LOADCELL_CALIBRATION_FACTOR = 2280.0; // Calibrate with standard 5kg weight
const float BIN_DEPTH_CM = 80.0;                  // Total depth of plate waste bin

void setup() {
  Serial.begin(115200);
  delay(1000);
  Serial.println("\n[ANNA-SETU] Initializing Smart IoT Intake Station...");

  // Pin Modes
  pinMode(PIN_US_TRIG, OUTPUT);
  pinMode(PIN_US_ECHO, INPUT);
  pinMode(PIN_LED_GREEN, OUTPUT);
  pinMode(PIN_LED_RED, OUTPUT);
  pinMode(PIN_BUZZER, OUTPUT);
  pinMode(PIN_RELAY_LOCK, OUTPUT);

  // Default state: Relays off, LEDs off
  digitalWrite(PIN_LED_GREEN, LOW);
  digitalWrite(PIN_LED_RED, LOW);
  digitalWrite(PIN_BUZZER, LOW);
  digitalWrite(PIN_RELAY_LOCK, LOW);

  // Initialize I2C Bus for MLX90614 IR sensor
  Wire.begin(21, 22);

  // Connect to Campus Wi-Fi
  connectToWiFi();

  // Self-test audio chime
  digitalWrite(PIN_BUZZER, HIGH);
  delay(100);
  digitalWrite(PIN_BUZZER, LOW);
  Serial.println("[ANNA-SETU] Hardware Station Online & Ready.");
}

void connectToWiFi() {
  Serial.print("[WiFi] Connecting to ");
  Serial.println(WIFI_SSID);
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);

  int attempts = 0;
  while (WiFi.status() != WL_CONNECTED && attempts < 20) {
    delay(500);
    Serial.print(".");
    attempts++;
  }

  if (WiFi.status() == WL_CONNECTED) {
    Serial.println("\n[WiFi] Connected! IP Address: " + WiFi.localIP().toString());
  } else {
    Serial.println("\n[WiFi] Connection timeout. Operating in offline buffered mode.");
  }
}

// Read ultrasonic distance to calculate plate waste volume fill percentage
float readPlateWasteFillPercentage() {
  digitalWrite(PIN_US_TRIG, LOW);
  delayMicroseconds(2);
  digitalWrite(PIN_US_TRIG, HIGH);
  delayMicroseconds(10);
  digitalWrite(PIN_US_TRIG, LOW);

  long duration = pulseIn(PIN_US_ECHO, HIGH, 30000);
  if (duration == 0) return 0.0;

  float distance_cm = duration * 0.034 / 2;
  float filled_depth = BIN_DEPTH_CM - distance_cm;
  if (filled_depth < 0) filled_depth = 0;
  
  float fill_percentage = (filled_depth / BIN_DEPTH_CM) * 100.0;
  return constrain(fill_percentage, 0.0, 100.0);
}

// Simulated/Real MLX90614 Contactless IR Surface Temp Reader
float readObjectSurfaceTemperature() {
  // In production, reads register 0x07 via I2C from MLX90614
  // Returns temperature in Celsius
  return 68.5; // Example reading (Hot holding active)
}

// Simulated/Real HX711 Weight Reader
float readNetWeightKg() {
  // In production, reads raw units from HX711 / LOADCELL_CALIBRATION_FACTOR
  return 18.5; // Example 18.5 kg vessel
}

void sendTelemetryPayload(float weight_kg, float temp_c, float fill_pct, const char* supervisor_id) {
  if (WiFi.status() != WL_CONNECTED) {
    Serial.println("[Telemetry] Wi-Fi offline. Buffering log...");
    return;
  }

  HTTPClient http;
  http.begin(API_ENDPOINT);
  http.addHeader("Content-Type", "application/json");

  // Construct JSON document
  StaticJsonDocument<512> doc;
  doc["station_id"] = STATION_ID;
  doc["supervisor_id"] = supervisor_id;
  doc["surplus_weight_kg"] = weight_kg;
  doc["surface_temp_c"] = temp_c;
  doc["plate_waste_fill_pct"] = fill_pct;
  doc["food_item"] = "Mixed Vegetable Pulao & Dal";
  doc["time_prepared"] = "12:30";
  doc["category_key"] = "cooked_grains_curry";
  doc["origin_zone"] = 4; // Gomti Nagar / Campus Zone

  String requestBody;
  serializeJson(doc, requestBody);

  Serial.println("[Telemetry] Transmitting to Anna-Setu Cloud...");
  int httpResponseCode = http.POST(requestBody);

  if (httpResponseCode > 0) {
    String response = http.getString();
    Serial.printf("[Telemetry] HTTP Response %d:\n%s\n", httpResponseCode, response.c_str());

    // Parse response verdict to trigger local actuator locks
    StaticJsonDocument<512> respDoc;
    deserializeJson(respDoc, response);
    const char* status = respDoc["status"];

    if (strcmp(status, "COMPLIANT_SAFE") == 0) {
      digitalWrite(PIN_LED_GREEN, HIGH);
      digitalWrite(PIN_LED_RED, LOW);
      digitalWrite(PIN_RELAY_LOCK, LOW);
    } else if (strcmp(status, "NON_COMPLIANT_REJECTED") == 0) {
      digitalWrite(PIN_LED_GREEN, LOW);
      digitalWrite(PIN_LED_RED, HIGH);
      // Sound alert and actuate bio-compost bin solenoid lock
      digitalWrite(PIN_RELAY_LOCK, HIGH); // Unlocks green compost bin only
      for (int i = 0; i < 3; i++) {
        digitalWrite(PIN_BUZZER, HIGH); delay(200);
        digitalWrite(PIN_BUZZER, LOW);  delay(100);
      }
    }
  } else {
    Serial.printf("[Telemetry] Error code: %d\n", httpResponseCode);
  }

  http.end();
}

void loop() {
  // Periodic sampling loop (e.g. check every 30 seconds or on button trigger)
  float weight = readNetWeightKg();
  float temp = readObjectSurfaceTemperature();
  float plate_fill = readPlateWasteFillPercentage();

  // If a significant weight is placed on the deck (> 2.0 kg), trigger handoff evaluation
  if (weight > 2.0) {
    Serial.printf("[Sensor Event] Weight: %.1f kg | Temp: %.1f C | Plate Waste Fill: %.1f%%\n", weight, temp, plate_fill);
    sendTelemetryPayload(weight, temp, plate_fill, "CHEF-UPES-01");
    delay(10000); // Debounce to prevent multiple sends
  }

  delay(2000);
}

