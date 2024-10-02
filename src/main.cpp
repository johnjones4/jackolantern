#include <Arduino.h>
#include <SPI.h>
#include <Adafruit_VS1053.h>
#include <SD.h>

#define SHIELD_RESET  -1      // VS1053 reset pin (unused!)
#define SHIELD_CS     7      // VS1053 chip select pin (output)
#define SHIELD_DCS    6      // VS1053 Data/command select pin (output)
#define CARDCS 4     // Card chip select pin
#define DREQ 3       // VS1053 Data request, ideally an Interrupt pin

Adafruit_VS1053_FilePlayer musicPlayer = Adafruit_VS1053_FilePlayer(SHIELD_RESET, SHIELD_CS, SHIELD_DCS, DREQ, CARDCS);

#define PIR_MOTION_SENSOR 9
#define DEBOUNCE 3000
#define MOTION_DELAY 10000

#define N_LIGHT_PINS 3
int lightPins[N_LIGHT_PINS] = {2, 5, 8};

unsigned long started = 0;
unsigned long lastMotion = 0;

void setup() {
  Serial.begin(9600);
  Serial.println("Starting up");

  if (! musicPlayer.begin()) { // initialise the music player
    Serial.println(F("Couldn't find VS1053, do you have the right pins defined?"));
    while (1);
  }

  Serial.println(F("VS1053 found"));

  if (!SD.begin(CARDCS)) {
    Serial.println(F("SD failed, or not present"));
    while (1);  // don't do anything more
  }
  Serial.println("SD OK!");

  pinMode(PIR_MOTION_SENSOR, INPUT);

  for (int i = 0; i < N_LIGHT_PINS; i++) {
    pinMode(lightPins[i], OUTPUT);
    digitalWrite(lightPins[i], HIGH);
    delay(500);
    digitalWrite(lightPins[i], LOW);
  }

  if (! musicPlayer.useInterrupt(VS1053_FILEPLAYER_PIN_INT)) {
    Serial.println(F("DREQ pin is not an interrupt pin"));
  }
}

void loop() {
  int motion = digitalRead(PIR_MOTION_SENSOR);
  if (motion && millis() - lastMotion > MOTION_DELAY) {
    if (started == 0) {
      started = millis();
    } else if (millis() - started > DEBOUNCE) {
      started = 0;
      Serial.println("Playing");
      musicPlayer.startPlayingFile("/laugh.mp3");
      while (musicPlayer.playingMusic) {
        int nextPin = random(N_LIGHT_PINS);
        int nextWait = random(50, 400);
        digitalWrite(lightPins[nextPin], HIGH);
        delay(nextWait);
        digitalWrite(lightPins[nextPin], LOW);
      }
      lastMotion = millis();
    }
  } else {
    started = 0;
  }
}
