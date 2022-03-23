#ifndef Barrier_h
#define Barrier_h
#include <Servo.h>
#include <Arduino.h>
#include "EthernetIO.h"

class Barrier
{
    public:
        Barrier(int pin, EthernetIO* ethernet);
        void open(EthernetIO* ethernet);
        void close(EthernetIO* ethernet);
    private:
        Servo _servo;
};

#endif
