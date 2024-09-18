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

#define PIR_MOTION_SENSOR 11
#define DEBOUNCE 10000

unsigned long started = 0;

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
}

void loop() {
  if (digitalRead(PIR_MOTION_SENSOR) && millis() - started >= DEBOUNCE) {
    started = millis();
    musicPlayer.startPlayingFile("/laugh.wav");
  }
}
