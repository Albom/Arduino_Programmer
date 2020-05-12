import time
import serial
import hashlib

NONE, C128, C256, C512, I04, I08, I16, I32, I64, I128, I256 = [i for i in range(11)]
sizes = (0, 0x4000, 0x8000, 0x10000, 0x200, 0x400, 0x800, 0x1000, 0x2000, 0x4000, 0x8000)


def prog_process(serial_port, mode, chip, filename):
    ic_size = sizes[chip]

    with serial.Serial(serial_port, 115200) as ser:

        time.sleep(1)

        command = b''.join([b'S', str(chip).encode(), b'\n'])
        ans =  ser.write(command)

        if mode == 'read':
            ans =  ser.write(b'R\n')
            data = [ser.read() for x in range(ic_size)]

            data = b''.join(data)

            with open(filename, 'wb') as file:
                file.write(bytes(data))

            hash = hashlib.md5(data).hexdigest()
            print(hash)
        elif mode == 'write':
            ans =  ser.write(b'W\n')
            with open(filename, 'rb') as file:
                data = bytearray(file.read(ic_size))

            for d in data:
                ans = ser.write(d.to_bytes(1, 'big'))
                rec = ser.read()

        else:
            pass

    print('OK')


if __name__ == '__main__':

    input_filename = 'test/rand8.bin'
    output_filename = 'test/out.bin'
    serial_port = '/dev/ttyACM0'
    chip = I08

    prog_process(serial_port, 'write', chip, input_filename)
    prog_process(serial_port, 'read', chip, output_filename)
