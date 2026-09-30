#include <DFRobot_HX711.h>

DFRobot_HX711 LoadCell(A0, A1);

void setup() {
  Serial.begin(115200);
}

void loop() {
  Serial.print(millis()/(float)1000, 2);
  Serial.print(",");
  Serial.println(LoadCell.readWeight(), 2);
}