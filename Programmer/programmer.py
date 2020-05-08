import time
import serial
import hashlib

NONE, C128, C256, C512, I04, I08, I16, I32, I64, I128, I256 = [i for i in range(11)]
sizes = (0, 0x4000, 0x8000, 0x10000, 0x200, 0x400, 0x800, 0x1000, 0x2000, 0x4000, 0x8000)

chip = I64

ic_size = sizes[chip]

mode = 'write'
mode = 'read'

input_filename = 'test/rand64.bin'

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
