#include <Arduino.h>
#include <Ethernet.h>
#include "BarrierSensor.h"
#include "Barrier.h"
#include "Bluetooth.h"
#include "EthernetIO.h"

BarrierSensor* barrierSensor1;
BarrierSensor* barrierSensor2;
Barrier* barrier;

byte mac[6] = { 0xBA, 0xDC, 0x0F, 0xFE, 0xC0, 0xDE };
IPAddress ip(192, 168, 1, 177);
EthernetIO* ethernet;

void setup() {
    Serial.begin(9600);
    ethernet = new EthernetIO(mac, ip, 23);
    barrierSensor1 = new BarrierSensor(2);
    barrierSensor2 = new BarrierSensor(3);
    barrier = new Barrier(9, ethernet);
    pinMode(7, OUTPUT);
}

bool is_msg_eth_open_gate(char* message) {
    if(message[0] == 'G' && message[1] == 'A' && message[2] == 'T' && message[3] == 0x42) {
        return true;
    }
    return false;
}

bool get_ethernet_message(char *buf) {
    bool got_it = ethernet->read_message(buf);
    if(got_it) {
        return true;
    }
    return false;
}

bool get_bluetooth_message(char *buf) {
    bool got_it = Bluetooth::get_message(buf);
    if(got_it) {
        return true;
    }
    return false;
}

char eth_buf[100];
char bt_buf[100];

void loop() {
    static bool lastbs1t = false;
    static bool lastbs2t = false;
    bool bs1t = barrierSensor1->is_triggered();
    bool bs2t = barrierSensor2->is_triggered();
    bool got_eth = get_ethernet_message(eth_buf);
    bool got_bt = get_bluetooth_message(bt_buf);
    if(bs1t) {
        if(got_eth && is_msg_eth_open_gate(eth_buf)) {
            barrier->open(ethernet);
            got_eth = false;
        }
    }
    else if(!bs2t && lastbs2t) {
        barrier->close(ethernet);
    }
    if(got_bt) {
        ethernet->write_message(bt_buf);
    }
    if(got_eth) {
        Bluetooth::send_message(eth_buf);
    }
    lastbs1t = bs1t;
    lastbs2t = bs2t;
    delay(100);
}
