import time
import serial
import hashlib
import sys
from PyQt5.QtWidgets import (QApplication, QMessageBox,
     QMainWindow, QGridLayout, QWidget, 
     QListWidget, QLabel, QLineEdit, QPushButton)
from PyQt5.QtGui import QPixmap

NONE, C128, C256, C512, I04, I08, I16, I32, I64, I128, I256 = [i for i in range(11)]
sizes = (0, 0x4000, 0x8000, 0x10000, 0x200, 0x400, 0x800, 0x1000, 0x2000, 0x4000, 0x8000)

input_filename = 'test/rand8.bin'
output_filename = 'test/out.bin'
serial_port = '/dev/ttyACM0'


class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setWindowTitle("Programmer")

        ic_types = ['None', '27C128', '27C256', '27C512', 
            '24C04', '24C08', '24C16', '24C32', '24C64', 
            '24C128', '24C256']
        self.ic_type_name = QListWidget()
        self.ic_type_name.addItems(ic_types)
        self.ic_type_name.setSortingEnabled(False)
        self.ic_type_name.itemClicked.connect(self.ic_click)

        self.image_none = QPixmap('images/panel-none.png')
        self.image_27 = QPixmap('images/panel-27.png')
        self.image_24 = QPixmap('images/panel-24.png')

        self.image = QLabel()
        self.image.setPixmap(self.image_none)

        self.line_port = QLineEdit()
        self.line_port.setText(serial_port)

        self.line_output = QLineEdit()
        self.line_output.setText(output_filename)

        self.line_input = QLineEdit()
        self.line_input.setText(input_filename)

        read_btn = QPushButton('Read')
        read_btn.clicked.connect(self.read_process)
        write_btn = QPushButton('Write')
        write_btn.clicked.connect(self.write_process)

        layout = QGridLayout()
        layout.addWidget(self.image, 0, 0)
        layout.addWidget(self.ic_type_name, 0, 1, 1, 3)
        layout.addWidget(QLabel('Port: '), 1, 1)
        layout.addWidget(self.line_port, 1, 2)
        layout.addWidget(QLabel('Output file: '), 2, 1)
        layout.addWidget(QLabel('Input file: '), 3, 1)
        layout.addWidget(self.line_output, 2, 2)
        layout.addWidget(self.line_input, 3, 2)
        layout.addWidget(read_btn, 2, 3)
        layout.addWidget(write_btn, 3, 3)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def ic_click(self, item):
        ic_27 = ('27C128', '27C256', '27C512')
        ic_24 = ('24C04', '24C08', '24C16', '24C32', '24C64', 
            '24C128', '24C256')
        if item.text() == 'None':
            self.image.setPixmap(self.image_none)
        elif item.text() in ic_27:
            self.image.setPixmap(self.image_27)
        elif item.text() in ic_24:
            self.image.setPixmap(self.image_24)

    def write_process(self):
        port = self.line_port.text()
        mode = 'write'
        chip = self.ic_type_name.currentRow()
        filename = self.line_input.text()
        r, t = prog_process(port, mode, chip, filename)
        self.show_msg(r, t)

    def read_process(self):
        port = self.line_port.text()
        mode = 'read'
        chip = self.ic_type_name.currentRow()
        filename = self.line_output.text()
        r, t = prog_process(port, mode, chip, filename)
        self.show_msg(r, t)

    def show_msg(self, r, t):
        msg = QMessageBox()
        if r:
            msg.setIcon(QMessageBox.Information)
            msg.setText('Operation complited. Hash sum (md5):\n' + t)
        else:
            msg.setIcon(QMessageBox.Critical)
            msg.setText('Error:\n' + t)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()


def prog_process(serial_port, mode, chip, filename):
    ic_size = sizes[chip]

    try:
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
                return (True, hash)

            elif mode == 'write':
                ans =  ser.write(b'W\n')
                with open(filename, 'rb') as file:
                    data = bytearray(file.read(ic_size))

                ret = []
                for d in data:
                    ans = ser.write(d.to_bytes(1, 'big'))
                    rec = ser.read()
                    ret.append(rec)

                ret = b''.join(ret)
                hash = hashlib.md5(ret).hexdigest()
                return (True, hash)

            else:
                return (False, None)

    except serial.SerialException:
        return (False, 'Serial port error')

if __name__ == '__main__':

    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    app.exec_()
