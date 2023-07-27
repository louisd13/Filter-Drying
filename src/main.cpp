/**
 * @file main.cpp
 * @author Louis Duval
 * @brief Arduino control & instructions
 * @version 0.1
 * @date 2023-06-29
 *
 * @copyright Copyright (c) 2023
 *
 */

#include <Arduino.h>
#include <Trustability_ABP_Gage.h>

#define EXP_TEMP // Change to your experience temperature (45/55/65)
// The differential value between inside and outside the capsule (depends on temperature)
#define delta_value  
// The actual temperature target from your external thermistor
#define TARGET_TEMP = EXP_TEMP - delta_value// 
#define sensorPin A0 // Arduino Pin for thermistor
#define slope_coeff 0.13 // has to be determine beforehand depending on the system [°C/s]
// Differential between measured temp and target temp threshold to activate the heating
const int temp_cutoff 1;   
// Differential value that dictates heating time depending on distance (in °C) to Target Temperature
const int temp_diff 5; 
// High Heating time : to change depending on the systems efficiency / inertia
const int high_time 45;
// low Heating time : to change depending on the systems efficiency / inertia
const int low_time 30;
const int initial_delay 30;
const int delay 10;
float pressure_amb = 0; // Ambient pressure initialization
bool switch_state = false; // Switch initialy off
const uint8_t PRESSURE1_PIN = 4; // Arduino pin for Pressure Sensor
Trustability_ABP_Gage pressure1;  // Pressure initialization


// Depending on the target temperature difference to temperature
// the wires are on for high_time or low_time [s] 
int uptime(int temp){
  if(temp + temp_diff < TARGET_TEMP){ 
    return high_time; 
  }
  else{
    return low_time;
  }
}

void read(){
  //Get a reading from the temperature sensor and pressure sensor:
  float reading = analogRead(sensorPin);
  float pressure = pressure1.getPressure() - pressure_amb;

  //Convert the reading into voltage:
  // (By default, the resolution of the readings is set at 10 bits, for compatibility with other Arduino boards.)
  float voltage = reading*(3.300 / 1024.000);

  //Convert the voltage into the temperature in degree Celsius: (Transfer function Datasheet)
  // (5/4.97) corrective term, 4.97 : Voltage of the thermistor measured with a multimeter
  float temp = (5/4.97)*(voltage - 1.375) / 0.0225;

  Serial.print(temp);
  Serial.println();
  Serial.print(pressure);
  Serial.println();
  Serial.println(switch_state);

  delay(1000); // 1 second delay
}

void enable_switch()
{
  switch_state = true;
  digitalWrite(42, HIGH); // sets the digital pin 42 on
}

void disable_switch()
{
  switch_state = false;
  digitalWrite(42, LOW); // sets the digital pin 42 off
}

void setup() {
  // SPI Init
  SPI.begin();

  // Hardware Init
  pressure1.begin(PRESSURE1_PIN, 3, "P1");

  // Begin serial communication at a baud rate of 9600:
  Serial.begin(9600);

  pinMode(42, OUTPUT);    // sets the digital pin 42 as output

  pressure_amb = pressure1.getPressure(); // a mettre la plus tot possible pour que les pompes soit éteintes 

  delay(3000);           // 3s delay time to start terminal
  enable_switch();       // activates the switch -> the heat is on

  // Average starting temperature determination
  float temp_avg = 0;
  int nb_avg = 100; // 100 values average 
  for(int i = 0; i < nb_avg ; i++){
  float reading = analogRead(sensorPin);
 // Convert the reading into voltage: (By default, the resolution of the readings is set at 10 bits, for compatibility with other Arduino boards.)
  float voltage = reading*(3.300 / 1024.000);
 // Convert the voltage into the temperature in degree Celsius: (Transfer function Datasheet)
  float temp = (voltage - 1.375) / 0.0225;
  temp_avg += temp;
  }
  temp_avg = temp_avg/nb_avg;

  // initial pulse determination depending on TARGET_TEMP and slope of the system in [°C/s]
  float initial_pulse_f = float((TARGET_TEMP-temp_avg)/(slope_coeff));
  int initial_pulse = int(initial_pulse_f); 
 
  
  for(int i = 0; i <= initial_pulse; i++){ // waits for X seconds, X given by initial_pulse
    read();  
    }

  // wait for thermal inertia delay of intial_delay seconds
  disable_switch();
  for(int i = 0; i < initial_delay; i++){
    read();
  }
}
  
void loop(){

  disable_switch();
  // Get a reading from the temperature sensor:
  float reading1 = analogRead(sensorPin);
  // Convert the reading into voltage: (By default, the resolution of the readings is set at 10 bits, for compatibility with other Arduino boards.)
  float voltage1 = reading1*(3.300 / 1024.000);
  // Convert the voltage into the temperature in degree Celsius: (Transfer function Datasheet)
  float temp1 = (voltage1 - 1.375) / 0.0225;


  if(temp1 < TARGET_TEMP - temp_cutoff){ // if the temperature measured is below the desired one with a delta of temp_cutoff
    enable_switch(); // switch on -> heat wires on 
    int uptime_delay = uptime(temp1);
    for(int i = 0; i <= uptime_delay; i++){ // time on dependant between target and actual temperature
      read();  
    }
    //wait for thermal inertia delay
    disable_switch();
    for(int i = 0; i < delay; i++){ //  delay (heat is off)
      read();
    }
  }
  else{
    read();
  }
}


