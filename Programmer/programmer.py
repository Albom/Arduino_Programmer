import time
import serial
import hashlib

NONE, C128, C256 = (0, 1, 2)
sizes = [0, 0x4000, 0x8000]

chip = C128

ic_size = sizes[chip]

with serial.Serial('/dev/ttyACM0', 115200) as ser:

    time.sleep(1)
    while ser.inWaiting():
        ans = ser.read(2)
    
    if ans != b'OK':
        exit()

    ans =  ser.write(b's1\n')

    ans =  ser.write(b'r\n')

    data = [ser.read() for x in range(ic_size)]

data = b''.join(data)

with open('out.bin', 'wb') as file:
    file.write(bytes(data))

hash = hashlib.md5(data).hexdigest()
print(hash)
print('OK')
