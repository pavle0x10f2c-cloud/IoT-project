

#include "esp_wifi.h"
#include <WiFi.h>
#include <WiFiUDP.h>
#include <WebServer.h>


// WiFi access point credentials
#ifndef APSSID
#define APSSID "paja"
#define APPSK "12345678"
#define UDP_TX_PACKET_MAX_SIZE 1460  // Set the maximum packet size (adjust as needed)
#endif

const char* ssid = APSSID;
const char* password = APPSK;
unsigned int localPort = 8888;  //UDP port to listen on
WebServer server(80);
char packetBuffer[UDP_TX_PACKET_MAX_SIZE+1];
char ReplayBuffer[]= "\r\n";
WiFiUDP Udp;
int led_DATA =0;       // LED level received from Python app
char led_CHAR ='o';   // character sent to Arduino over Serial

// handles HTTP ping from Python app to check if ESP is reachable
void handleRoot(){
  server.send(200,"text/html","<h1> Connected </h1>");
}

void setup() {
  delay(1000);
  Serial.begin(9600);             // Serial communication with Arduino
  WiFi.softAP(ssid,password);    // start WiFi access point
  Udp.begin(localPort);         // start listening for UDP packets
  server.on("/",handleRoot);
  server.begin();
}
void loop(){
  server.handleClient();    // handle HTTP ping requests
  int packetSize = Udp.parsePacket();
  if(packetSize){
    // read incoming UDP packet
    int n = Udp.read(packetBuffer,UDP_TX_PACKET_MAX_SIZE);
    packetBuffer[n]=0;
    // convert received string to integer LED level
    led_DATA =((String)(packetBuffer)).toInt();
    
    // map LED level to a character to send to Arduino via Serial
    if (led_DATA == 0){
      led_CHAR = 'o';
    }else if(led_DATA==11){
      led_CHAR = 'a';
    }else if (led_DATA==12){
      led_CHAR = 'b';
    }else{
      led_CHAR =((String)(led_DATA-1)).charAt(0);
    }
    Serial.write(led_CHAR);  // send level to Arduino
    
    // send confirmation back to Python app
    Udp.beginPacket(Udp.remoteIP(),Udp.remotePort());
        size_t length = strlen(ReplayBuffer);  // Get the length of the message

    Udp.write((uint8_t*)ReplayBuffer,length);
    Udp.endPacket();
  }
}


