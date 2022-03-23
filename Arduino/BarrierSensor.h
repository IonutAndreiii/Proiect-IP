#ifndef BarrierSensor_h
#define BarrierSensor_h
#include <Arduino.h>

class BarrierSensor
{
    public:
        BarrierSensor(int pin);
        bool is_triggered();
    private:
        int _pin;
};

#endif