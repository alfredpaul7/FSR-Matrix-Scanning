//C++ code for 32x32 with serial communication
#include<Arduino.h>
// --- 74HC595 Pin Definitions (Drive 32 Columns) ---
const int ser    = 13; 
const int srclk  = 12; 
const int rclk  = 11; 
// --- CD74HC4067 Pin Definitions (Read line 32) ---
const int sPins[]  = {2, 3, 4, 5};// Address lines S0, S1, S2, S3
const int rowA     = A0;           // MUX 1 output (Row 1-16)
const int rowB     = A1;           // MUX 2 output (Row 17-32)
void setActiveColumn(int col);
void clearAllColumns();
void clearAllColumns();
void setup() {
  // Use a high baud rate to ensure fast transmission of 1,024 points.
  Serial.begin(115200);
  // Initialize 595 control pin
  pinMode(ser, OUTPUT);//ser sending bit value to the register
  pinMode(srclk, OUTPUT);//srclk  sending the data insidethe resister
  pinMode(rclk, OUTPUT);//rclk updates output all at once  latch 
  // Initialize MUX address control pins
  for (int i = 0; i < 4; i++) {
    pinMode(sPins[i], OUTPUT);
  }
  // Initial state: clear all columns
  clearAllColumns();  
}
void loop() {
  // Iterate through 32 columns (1 ~ 32)
  for (int col = 1; col <= 32; col++) {
    // 1. Power on the current column (3.3V)
    setActiveColumn(col);
    // 2. Switch MUX to read the 32 rows in the current column
    // Because there are two MUXs connected to A0 and A1 respectively, it only takes 16 loops to read all 32 rows.
    for (int ch = 0; ch < 16; ch++) {
      // Set the 4-bit address of the MUX (S0-S3))
      digitalWrite(sPins[0], (ch & 0x01));
      digitalWrite(sPins[1], (ch >> 1) & 0x01);
      digitalWrite(sPins[2], (ch >> 2) & 0x01);
      digitalWrite(sPins[3], (ch >> 3) & 0x01);
      // Provides an extremely short settling time for the analog signal (stabilizing voltage divider circuit)
      delayMicroseconds(30);
      // Read A0 (Row 1-16) and A1 (Row 17-32)
      int val1 = analogRead(rowA); 
      int val2 = analogRead(rowB);
      // --- Output data for Python to parse ---
      // Output format: val,val,val...
      Serial.print(val1);
      Serial.print(",");
      Serial.print(val2);
      // Add a comma if it's not the last point in the entire image.
      if (ch < 15 || col < 32) {
        Serial.print(",");
      }
    }
  }
 // Once all 1,024 dots have been transmitted, a newline character is sent.
  Serial.println();
}
// --- Core function: Precisely selects a specific column from 32 bits ---
void setActiveColumn(int col) { 
  // Preparing for an update, first lower the latch
  digitalWrite(rclk, LOW);
  // 4 595 cascaded chips require a total of 32 bits to be transferred
  // Here, the transfer starts from the 32nd bit and moves to the 1st bit (FIFO, pushed to the last chip)
  for (int i = 32; i >= 1; i--) {
    digitalWrite(srclk, LOW);
    // Only the target is listed as HIGH, the rest as LOW.
    if (i == col) {
      digitalWrite(ser, HIGH);
    } else {
      digitalWrite(ser, LOW);
    }
    digitalWrite(srclk, HIGH);// Input bit
  }
  // Transfer complete, pull the latch high to update the output status
  digitalWrite(rclk, HIGH);
}
// --- Helper function: Clear the voltage of all columns ---
void clearAllColumns() {
  digitalWrite(rclk, LOW);
  for (int i = 0; i < 32; i++) {
    digitalWrite(srclk, LOW);
    digitalWrite(ser, LOW);
    digitalWrite(srclk, HIGH);
  }
  digitalWrite(rclk, HIGH);
}
