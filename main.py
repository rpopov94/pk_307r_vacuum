from spk_307 import Spk_Dialog
from PyQt5 import QtWidgets
from PyQt5 import QtCore
from pymodbus.client.sync import ModbusTcpClient
from settings import ip


class SPK(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.client = ModbusTcpClient(ip)
        self.client.connect()
        self.w_root = Spk_Dialog()
        self.w_root.setupUi(self)
        self.w_root.st_mption_1.clicked.connect(self.first_motion_control)
        self.w_root.st_motion_2.clicked.connect(self.second_motion_control)
        self.w_root.valve_11.clicked.connect(self.valve11_control)
        self.w_root.valve_12.clicked.connect(self.valve12_control)
        self.w_root.valve_21.clicked.connect(self.valve21_control)
        self.w_root.valve_22.clicked.connect(self.valve21_control)
        self.w_root.manage.clicked.connect(self.manage_control)
        self.w_root.stop.clicked.connect(self.stop_cotrol)
        self.w_root.settings.clicked.connect(self.settings_cotrol)

    def first_motion_control(self):
        print('first_motion_control')
        address = 260
        try:
            result = self.client.read_coils(address)
            if result.read_bits[0]:
                self.client.write_coil(address, 0)
            self.client.write_coil(address, 1)
        except:
            print('first_motion_control')

    def second_motion_control(self):
        print('second_motion_control')
        address = 261
        result = self.client.read_coils(address)
        if result.read_bits[0]:
            self.client.write_coil(address, 0)
        self.client.write_coil(address, 1)

    def valve11_control(self):
        print('valve11_control')
        # self.client.write_coil(280, 1)
        address = 280
        result = self.client.read_coils(address)
        if result.read_bits[0]:
            self.client.write_coil(address, 0)
        self.client.write_coil(address, 1)

    def valve12_control(self):
        print('valve12_control')
        # self.client.write_coil(281, 1)
        address = 281
        result = self.client.read_coils(address)
        if result.read_bits[0]:
            self.client.write_coil(address, 0)
        self.client.write_coil(address, 1)

    def valve21_control(self):
        print('valve21_control')
        # self.client.write_coil(282, 1)
        address = 282
        result = self.client.read_coils(address)
        if result.read_bits[0]:
            self.client.write_coil(address, 0)
        self.client.write_coil(address, 1)

    def valve22_control(self):
        print('valve22_control')
        # self.client.write_coil(283, 1)
        address = 283
        result = self.client.read_coils(address)
        if result.read_bits[0]:
            self.client.write_coil(address, 0)
        self.client.write_coil(address, 1)

    def manage_control(self):
        print('manage_control')

    def stop_cotrol(self):
        print('stop_cotrol')

    def settings_cotrol(self):
        print('settings_cotrol')


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication([])
    application = SPK()
    application.show()
    sys.exit(app.exec())

# client.close()
