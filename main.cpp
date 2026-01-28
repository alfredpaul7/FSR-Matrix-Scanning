//C++ code for 32x64 with SPI protocol
#include <Arduino.h>
#include <SPI.h>

// --- SPI Pin Definitions ---
/*RCLK D10
SRCLK  D13
SER D11*/
const int slaveSelectPin = 10; 
// --- CD74HC4067 Pin Definitions ---
const int sPins[] = {2, 3, 4, 5};
// --- Analog Rows ---
// Sensor 1 (Left)
const int rowA = A0; 
const int rowB = A1; 
// Sensor 2 (Right)
const int rowC = A2; 
const int rowD = A3; 
void setActiveColumn(int col);
void clearAllColumns();
void setMuxAddress(int ch);
void setup() {
  Serial.begin(921600);
  pinMode(slaveSelectPin, OUTPUT);
  digitalWrite(slaveSelectPin, HIGH);
  SPI.begin();
  SPI.beginTransaction(SPISettings(8000000, MSBFIRST, SPI_MODE0));
  for (int i = 0; i < 4; i++) {
    pinMode(sPins[i], OUTPUT);
  }
  clearAllColumns();
}
void loop() {
  // --- PART 1: READ SENSOR 1 (Left) ---
  for (int col = 0; col < 32; col++) {
    setActiveColumn(col);
    for (int ch = 0; ch < 16; ch++) {
      setMuxAddress(ch);
      delayMicroseconds(20); 
      Serial.print(analogRead(rowA));
      Serial.print(",");
      Serial.print(analogRead(rowB));
      Serial.print(","); // Always trailing comma here
    }
  }
  // --- PART 2: READ SENSOR 2 (Right) ---
  for (int col = 0; col < 32; col++) {
    setActiveColumn(col);
    for (int ch = 0; ch < 16; ch++) {
      setMuxAddress(ch);
      delayMicroseconds(20); 
      Serial.print(analogRead(rowC));
      Serial.print(",");
      Serial.print(analogRead(rowD));
      // Only add comma if it's NOT the very last value of the whole 2048 set
      if (ch < 15 || col < 31) {
        Serial.print(",");
      }
    }
  }
  Serial.println(); // Single Newline to end the 2048-value frame
}
void setMuxAddress(int ch) {
  digitalWrite(sPins[0], (ch & 0x01));
  digitalWrite(sPins[1], (ch >> 1) & 0x01);
  digitalWrite(sPins[2], (ch >> 2) & 0x01);
  digitalWrite(sPins[3], (ch >> 3) & 0x01);
}
void setActiveColumn(int col) {
  uint32_t bitmask = 0x00000001UL << col;
  digitalWrite(slaveSelectPin, LOW);
  SPI.transfer((bitmask >> 24) & 0xFF);
  SPI.transfer((bitmask >> 16) & 0xFF);
  SPI.transfer((bitmask >> 8) & 0xFF);
  SPI.transfer(bitmask & 0xFF);
  digitalWrite(slaveSelectPin, HIGH);
}
void clearAllColumns() {
  digitalWrite(slaveSelectPin, LOW);
  for(int i=0; i<4; i++) SPI.transfer(0);
  digitalWrite(slaveSelectPin, HIGH);
}