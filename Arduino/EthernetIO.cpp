#include "EthernetIO.h"

EthernetIO::EthernetIO(byte* mac, IPAddress ip, int port) {
    EthernetClient client;
    Ethernet.begin(mac, ip);
    server = new EthernetServer(port);
    server->begin();
    pinMode(7, OUTPUT);
    digitalWrite(7, HIGH);
    do {
        client = server->available();
    } while(client.available() <= 0);
    client.read();
    digitalWrite(7, LOW);
}

void EthernetIO::write_message(char* message) {
    server->write(message);
}

bool EthernetIO::read_message(char* message) {
    EthernetClient client = server->available();
    if(client.available() > 0) {
        int no_chars = 0;
        byte thisChar = client.read();
        while(thisChar!=255) {
            message[no_chars] = thisChar;
            no_chars++;
            thisChar = client.read();
        }
        if(no_chars > 0) {
            return true;
        }
    }
    return false;
}

void EthernetIO::send_gate_closed() {
    char GATE_CLOSED_MESSAGE[5] = {0x47, 0x41, 0x54, 0x04};
    write_message(GATE_CLOSED_MESSAGE);
}

void EthernetIO::send_gate_opened() {
    char GATE_OPENED_MESSAGE[5] = {0x47, 0x41, 0x54, 0x02};
    write_message(GATE_OPENED_MESSAGE);
}

void EthernetIO::send_gate_closing() {
    char GATE_CLOSING_MESSAGE[5] = {0x47, 0x41, 0x54, 0x03};
    write_message(GATE_CLOSING_MESSAGE);
}

void EthernetIO::send_gate_opening() {
    char GATE_OPENING_MESSAGE[5] = {0x47, 0x41, 0x54, 0x01};
    write_message(GATE_OPENING_MESSAGE);
}