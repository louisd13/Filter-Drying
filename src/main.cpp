#include <Arduino.h>
#include <Trustability_ABP_Gage.h>


#define sensorPin A0
float pressure_amb = 0;
const uint8_t PRESSURE1_PIN = 4;
Trustability_ABP_Gage pressure1; 
 
void read(){
 // Get a reading from the temperature sensor and pressure sensor:
  float reading = analogRead(sensorPin);
  float pressure = pressure1.getPressure() - pressure_amb;

 // Convert the reading into voltage: (By default, the resolution of the readings is set at 10 bits, for compatibility with other Arduino boards.)
  float voltage = reading*(3.300 / 1024.000);

 // Convert the voltage into the temperature in degree Celsius: (Transfer function Datasheet)
  float temp = (voltage - 1.375) / 0.0225;

  Serial.print(temp);
  Serial.println();
  Serial.print(pressure);
  Serial.println();

  delay(1000);
}

void setup() {
  // SPI Init
  SPI.begin();

  // Hardware Init
  pressure1.begin(PRESSURE1_PIN, 3, "P1");

  // Begin serial communication at a baud rate of 9600:
  Serial.begin(9600);

  pinMode(42, OUTPUT);    // sets the digital pin 42 as output
  digitalWrite(42, HIGH); // sets the digital pin 42 on

  pressure_amb = pressure1.getPressure();

  for(int i = 0; i <= 180; i++){ // waits for 180 seconds 
    read();  
  }
}
  
void loop() {

  digitalWrite(42, LOW);
  // Get a reading from the temperature sensor:
  float reading1 = analogRead(sensorPin);
 // Convert the reading into voltage: (By default, the resolution of the readings is set at 10 bits, for compatibility with other Arduino boards.)
  float voltage1 = reading1*(3.300 / 1024.000);
 // Convert the voltage into the temperature in degree Celsius: (Transfer function Datasheet)
  float temp1 = (voltage1 - 1.375) / 0.0225;
  if(temp1 < 53){ // Objectif of °C 
    digitalWrite(42, HIGH); // sets the digital pin 42 on
    for(int i = 0; i <= 20; i++){ // waits for 20 seconds 
      read();  
    }
  }
  if(temp1 > 58){ // Seuil max °C inutile je crois 
    digitalWrite(42, LOW);
  }
  read();
}


