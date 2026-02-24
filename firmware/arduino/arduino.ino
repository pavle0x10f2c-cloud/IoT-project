#include <SoftwareSerial.h>

// pins 2,3 used for Serial communication with ESP32
SoftwareSerial espSerial(2, 3);

void setup() {
  // set pins 2-13 as output (each pin controls one LED)
  for(int pin = 2; pin <= 13; pin++){
    pinMode(pin, OUTPUT);
    digitalWrite(pin, LOW);  // all LEDs off at start
  }

  Serial.begin(9600);     // Serial monitor
  espSerial.begin(9600);  // Serial communication with ESP32
}

char data = 'o';  // current LED level, 'o' = all off

// turns on LEDs from pin 2 up to the given pin, turns rest off
void turn_on_leds(int pin){
  for(int i = 2; i <= 13; i++){
    digitalWrite(i, LOW);
  }
  for(int i = 2; i <= pin; i++){
    delay(2);
    digitalWrite(i, HIGH);
  }
  data = 'r';
}

void loop() {
  // read character from ESP32 if available
  if(Serial.available() > 0){
    data = (char) Serial.read();
  }

  // map character to LED pin count
  // 0-9 = pins 2-11, a = pin 12, b = pin 13, o = all off
  switch(data){
    case '0': turn_on_leds(2);  break;
    case '1': turn_on_leds(3);  break;
    case '2': turn_on_leds(4);  break;
    case '3': turn_on_leds(5);  break;
    case '4': turn_on_leds(6);  break;
    case '5': turn_on_leds(7);  break;
    case '6': turn_on_leds(8);  break;
    case '7': turn_on_leds(9);  break;
    case '8': turn_on_leds(10); break;
    case '9': turn_on_leds(11); break;
    case 'a': turn_on_leds(12); break;
    case 'b': turn_on_leds(13); break;
    case 'o': turn_on_leds(0);  break;
    default: break;
  }
}
