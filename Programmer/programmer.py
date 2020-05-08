import time
import serial
import hashlib

NONE, C128, C256, C512, I08, I16, I32, I64 = (0, 1, 2, 3, 4, 5, 6, 7)
sizes = (0, 0x4000, 0x8000, 0x10000, 0x400, 0x800, 0x1000, 0x2000)

chip = I16

ic_size = sizes[chip]

#mode = 'write'
mode = 'read'

input_filename = 'test/rand16.bin'

with serial.Serial('/dev/ttyACM0', 115200) as ser:

    time.sleep(1)

    command = b''.join([b'S', str(chip).encode(), b'\n'])
    ans =  ser.write(command)

    if mode == 'read':
        ans =  ser.write(b'R\n')
        data = [ser.read() for x in range(ic_size)]

        data = b''.join(data)

        with open('test/out.bin', 'wb') as file:
            file.write(bytes(data))

        hash = hashlib.md5(data).hexdigest()
        print(hash)
    elif mode == 'write':
        ans =  ser.write(b'W\n')
        with open(input_filename, 'rb') as file:
            data = bytearray(file.read(ic_size))

        for d in data:
            ans = ser.write(d.to_bytes(1, 'big'))
            rec = ser.read()

    else:
        pass

print('OK')
