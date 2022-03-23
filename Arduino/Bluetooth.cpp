#include "Bluetooth.h"

Bluetooth::Bluetooth() {
    Serial.begin(9600);
    Serial.flush();
}

bool Bluetooth::get_message(char* buf) {
    char val;
    int k = 0;

    if(Serial.available() > 0) {
        val = Serial.read();
        if(val == -1) {
            return false;
        }
        while(val != -1) {
            buf[k] = val;
            k++;
            val = Serial.read();
        }
        return true;
    }
    return false;
}

void Bluetooth::send_message(char* message) {
    Serial.write(message);
    Serial.flush();
}

void Bluetooth::send_gate_closed() {
    char GATE_CLOSED_MESSAGE[5] = {0x47, 0x41, 0x54, 0x04};
    Serial.write(GATE_CLOSED_MESSAGE);
    Serial.flush();
}

void Bluetooth::send_gate_opened() {
    char GATE_OPENED_MESSAGE[5] = {0x47, 0x41, 0x54, 0x02};
    Serial.write(GATE_OPENED_MESSAGE);
    Serial.flush();
}

void Bluetooth::send_gate_closing() {
    char GATE_CLOSING_MESSAGE[5] = {0x47, 0x41, 0x54, 0x03};
    Serial.write(GATE_CLOSING_MESSAGE);
    Serial.flush();
}

void Bluetooth::send_gate_opening() {
    char GATE_OPENING_MESSAGE[5] = {0x47, 0x41, 0x54, 0x01};
    Serial.write(GATE_OPENING_MESSAGE);
    Serial.flush();
}