import time
import serial
import hashlib

NONE, C128, C256, C512 = (0, 1, 2, 3)
sizes = (0, 0x4000, 0x8000, 0x10000)

chip = C512

ic_size = sizes[chip]

with serial.Serial('/dev/ttyACM0', 115200) as ser:

    time.sleep(1)

    command = b''.join([b's', str(chip).encode(), b'\n'])
    ans =  ser.write(command)

    ans =  ser.write(b'r\n')

    data = [ser.read() for x in range(ic_size)]

data = b''.join(data)

with open('out.bin', 'wb') as file:
    file.write(bytes(data))

hash = hashlib.md5(data).hexdigest()
print(hash)
print('OK')
