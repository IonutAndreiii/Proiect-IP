#include "BarrierSensor.h"

BarrierSensor::BarrierSensor(int pin) {
    pinMode(pin, INPUT_PULLUP);
    _pin = pin;
}

bool BarrierSensor::is_triggered() {
    return digitalRead(_pin) == 0;
}