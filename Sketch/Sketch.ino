#include <Wire.h>

const int nOE = 8;
const int nCE = 9;

const int I2C_ADDR = 0x50;

typedef enum {
  NONE,
  C128,
  C256,
  C512,
  I08,
  I16,
  I32,
  I64
} Chip;


int chip = NONE;

const int MAX_LEN = 16;
char command[MAX_LEN];

void eeprom_write_byte_64(byte dev, uint16_t address, byte data)
{
  Wire.beginTransmission(dev);
  Wire.write(address >> 8);
  Wire.write(address & 0xFF);
  Wire.write(data);
  delay(5);
  Wire.endTransmission();
}


byte eeprom_read_byte_64(int dev, uint16_t address) {
  Wire.beginTransmission(dev);
  Wire.write(address >> 8);
  Wire.write(address & 0xFF);
  Wire.endTransmission();
  Wire.requestFrom(dev, (byte)1);
  byte rdata = 0;
  if (Wire.available()) {
    rdata = Wire.read();
  }
  return rdata;
}



void eeprom_write_byte_16(byte dev, uint16_t address, byte data)
{
  uint8_t addr_m = dev | ((address >> 8) & 0x07);
  Wire.beginTransmission(addr_m);
  Wire.write(address & 0xFF);
  Wire.write(data);
  delay(5);
  Wire.endTransmission();
}

byte eeprom_read_byte_16(int dev, uint16_t address) {
  uint8_t addr_m = dev | ((address >> 8) & 0x07);
  Wire.beginTransmission(addr_m);
  Wire.write(address & 0xFF);
  Wire.endTransmission();
  Wire.requestFrom(addr_m, (byte)1);
  byte rdata = 0xFF;
  if (Wire.available()) {
    rdata = Wire.read();
  }
  return rdata;
}


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

  Wire.begin();
  Wire.setClock(100000);
}


uint32_t get_chip_size() {

  uint32_t ic_size = 0; // for future support of >64 kBytes chips

  switch (chip) {
    case I08:
      ic_size = 0x400;
      break;
    case I16:
      ic_size = 0x800;
      break;
    case I32:
      ic_size = 0x1000;
      break;
    case I64:
      ic_size = 0x2000;
      break;
    case C128:
      ic_size = 0x4000;
      break;
    case C256:
      ic_size = 0x8000;
      break;
    case C512:
      ic_size = 0x10000;
      break;
    default:
      ic_size = 0;
  }
  return ic_size;
}

void read_chip() {

  uint32_t ic_size = get_chip_size();

  switch (chip) {
    case C128:
    case C256:
    case C512:

      for (uint32_t addr = 0; addr < ic_size; addr++) {
        PORTF = addr >> 8;
        PORTK = addr & 0xFF;

        // PORTF |= 0b01100000; // D27128

        digitalWrite(nOE, LOW);
        delayMicroseconds(10);
        Serial.write(PINC);
        digitalWrite(nOE, HIGH);
      }
      break;

    case I64:
      for (uint32_t addr = 0; addr < ic_size; addr++) {
        byte c = eeprom_read_byte_64(I2C_ADDR, (uint16_t) addr);
        Serial.write(c);
      }
      break;

    case I08:
    case I16:
      for (uint32_t addr = 0; addr < ic_size; addr++) {
        byte c = eeprom_read_byte_16(I2C_ADDR, (uint16_t) addr);
        Serial.write(c);
      }
      break;

    default:
      break;

  }
}



void write_chip() {

  uint32_t ic_size = get_chip_size();
  uint32_t addr = 0;

  switch (chip) {

    case I08:
    case I16:
      while (addr < ic_size) {
        if (Serial.available() > 0) {
          byte c = Serial.read();
          eeprom_write_byte_16(I2C_ADDR, (uint16_t) addr, c);
          Serial.write(c);
          addr++;
        }
      }
      break;


    case I64:
      while (addr < ic_size) {
        if (Serial.available() > 0) {
          byte c = Serial.read();
          eeprom_write_byte_64(I2C_ADDR, (uint16_t) addr, c);
          Serial.write(c);
          addr++;
        }
      }
      break;

    default:
      break;


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
    case '3':
      chip = C512;
      break;
    case '4':
      chip = I08;
      break;
    case '5':
      chip = I16;
      break;
    case '6':
      chip = I32;
      break;
    case '7':
      chip = I64;
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
    case 'W':
      write_chip();
      break;
    default:
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

