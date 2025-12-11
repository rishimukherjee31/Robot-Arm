#include <Stepper.h>
#include <Encoder.h>

#define STEPS_PER_REV 500
#define DIR_PIN 3
#define STEP_PIN 2
#define ENABLE_PIN 4
#define ENC_A 5
#define ENC_B 6
#define ENC_Z 7
#define PRINT_HZ 1000 // Publishing frequency in Hz

Stepper myStepper(STEPS_PER_REV, DIR_PIN, STEP_PIN);
Encoder motorEncoder(ENC_A, ENC_B);

IntervalTimer printTimer;

void publishEncoder() {
  long encoderPos = motorEncoder.read();
  Serial.println(encoderPos);
}

void setup() {
  Serial.begin(2000000);
  pinMode(ENABLE_PIN, OUTPUT);
  digitalWrite(ENABLE_PIN, LOW);
  myStepper.setSpeed(60);
  pinMode(ENC_Z, INPUT);
  
  printTimer.begin(publishEncoder, 1000000 / PRINT_HZ);
}

void loop() {
  // forward one revolution
  myStepper.step(STEPS_PER_REV);
  delay(1000);
  
  // backward one revolution
  myStepper.step(-STEPS_PER_REV);
  delay(1000);
}