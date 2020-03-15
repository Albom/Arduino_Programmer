const int nOE = 8;
const int nCE = 9;

int mode = 0;

void setup() {

  pinMode(nOE, OUTPUT);
  digitalWrite(nOE, HIGH);

  pinMode(nCE, OUTPUT);
  digitalWrite(nCE, LOW);

  DDRF = 0xFF;
  DDRK = 0xFF;

  DDRC = 0;
  PORTC = 0xFF;

  Serial.begin(115200);

}

void loop() {
  uint16_t addr = 0;

  if (Serial.available() > 0) {

    int b = Serial.read();
    if (b == 'r') {
      mode = 1;
    }
  }

  if (mode == 1) {
    for (addr = 0; addr < 0x4000; addr++) {
      PORTF = addr >> 8;
      PORTK = addr & 0xFF;
      digitalWrite(nOE, LOW);
      delayMicroseconds(10);
      Serial.write(PINC);
      digitalWrite(nOE, HIGH);
    }
  }
  mode = 0;
}

