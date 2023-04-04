#ifndef TRUSTABILITY_ABP_GAGE_H
#define TRUSTABILITY_ABP_GAGE_H

#include <Arduino.h>
#include <SPI.h>

class Trustability_ABP_Gage
{

private:
    int pin_slave_select;
    float pressure = 0;
    float temperature = 0;
    String ID = "no_ID";
    float max_pressure = 3.2; // in bar
    uint32_t last_reading = 0;

public:
    void begin(byte _pin_slave_select, float _max_pressure);
    void begin(byte _pin_slave_select, float _max_pressure, String _name);
    void read();
    float getPressure();
    float getTemperature();
    float getMaxPressure();
    String getID();
};


// inutile ??
void TC3_Handler();
#endif