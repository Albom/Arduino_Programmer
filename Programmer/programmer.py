import time
import serial
import hashlib

with serial.Serial('/dev/ttyACM0', 115200) as ser:

    time.sleep(1)
    x =  ser.write(b'r')

    data = [ser.read() for x in range(0x4000)]

data = b''.join(data)

with open('out.bin', 'wb') as file:
    file.write(bytes(data))

hash = hashlib.md5(data).hexdigest()
print(hash)
print('OK')
