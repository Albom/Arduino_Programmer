const int nOE = 8;
const int nCE = 9;

typedef enum {
  NONE,
  C128,
  C256
} Chip;


int chip = NONE;

const int MAX_LEN = 16;
char command[MAX_LEN];


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

void read_chip() {

  uint16_t ic_size = 0;
  switch (chip) {
    case C128:
      ic_size = 0x4000;
      break;
    case C256:
      ic_size = 0x8000;
      break;
    default:
      ic_size = 0;
  }
  for (uint16_t addr = 0; addr < ic_size; addr++) {
    PORTF = addr >> 8;
    PORTK = addr & 0xFF;
    digitalWrite(nOE, LOW);
    delayMicroseconds(10);
    Serial.write(PINC);
    digitalWrite(nOE, HIGH);
  }
}


void set_chip() {
  switch (command[1]) {
    case '1':
      chip = C128;
      break;
    case '2':
      chip = C256;
      break;
    default:
      chip = NONE;
  }
}


void exec_command() {

  switch (command[0]) {
    case 'R':
      read_chip();
      break;
    case 'S':
      set_chip();
      break;
  }
}

void loop() {

  int len = 0;
  bool currentCommand = true;
  while (currentCommand) {
    if (Serial.available() > 0) {
      char c = Serial.read();
      switch (c) {
        case '\r':
        case ' ':
          break;
        case '\n':
          if (len > 0) {
            command[len] = '\0';
            exec_command();
            currentCommand = false;
          }
          break;
        default:
          if (len < MAX_LEN - 1) {
            command[len++] = ( c >= 'a' && c <= 'z' ) ? c - 'a' + 'A' : c;
          }
      }
    }
  }

}

