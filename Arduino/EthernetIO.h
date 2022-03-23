#ifndef EthernetIO_h
#define EthernetIO_h
#include <SPI.h>
#include <Arduino.h>
#include <Ethernet.h>

class EthernetIO
{
    public:
        EthernetIO(byte* mac, IPAddress ip, int port);
        void write_message(char* message);
        bool read_message(char *buf);
        void send_gate_closed();
        void send_gate_opened();
        void send_gate_closing();
        void send_gate_opening();
    private:
        EthernetServer *server;
};

#endif
