#ifndef Bluetooth_h
#define Bluetooth_h
#include <Arduino.h>

class Bluetooth
{
    public:
        Bluetooth();
        static bool get_message(char *buf);
        static void send_message(char *message);
        static void send_gate_closed();
        static void send_gate_opened();
        static void send_gate_closing();
        static void send_gate_opening();
};

#endif
