#include "Servo.h"

#define GRIPPER_PWM_PIN   10
#define OPEN_PWM_US       1100
#define CLOSE_PWM_US      1900
#define STOP_PWM_US       1500

Servo gripper;

void setup() {
  Serial.begin(57600);
  gripper.attach(GRIPPER_PWM_PIN);
  gripper.writeMicroseconds(STOP_PWM_US);
}

void loop() {
  if (Serial.available() > 0) {
    char cmd = Serial.read();
    switch (cmd) {
      case 'O': gripper.writeMicroseconds(OPEN_PWM_US);  break;
      case 'C': gripper.writeMicroseconds(CLOSE_PWM_US); break;
      case 'S': gripper.writeMicroseconds(STOP_PWM_US);  break;
    }
  }
}
