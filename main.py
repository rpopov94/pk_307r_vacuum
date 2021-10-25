from spk_307 import Ui_Dialog
from PyQt5 import QtWidgets
from PyQt5 import QtCore
from pymodbus.client.sync import ModbusTcpClient
from settings import ip
from utilites import Utilites
import datetime


class BrowserHandler(QtCore.QObject):
    newTextAndColor = QtCore.pyqtSignal()

    def run(self):
        while True:
            self.newTextAndColor.emit()
            QtCore.QThread.msleep(1000)


class SPK(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.w_root = Ui_Dialog()
        self.w_root.setupUi(self)
        self.client = ModbusTcpClient(ip)
        self.client.connect()
        self.w_root.st_mption_1.clicked.connect(self.first_motion_control)
        self.w_root.st_motion_2.clicked.connect(self.second_motion_control)
        self.w_root.valve_11.clicked.connect(self.valve11_control)
        self.w_root.valve_12.clicked.connect(self.valve12_control)
        self.w_root.valve_21.clicked.connect(self.valve21_control)
        self.w_root.valve_22.clicked.connect(self.valve22_control)
        self.w_root.manage.clicked.connect(self.manage_control)
        self.w_root.stop.clicked.connect(self.stop_cotrol)
        self.w_root.settings.clicked.connect(self.settings_cotrol)

        self.thread = QtCore.QThread()
        self.browserHandler = BrowserHandler()
        self.browserHandler.moveToThread(self.thread)
        self.browserHandler.newTextAndColor.connect(self.moitor)
        self.thread.started.connect(self.browserHandler.run)
        self.thread.start()


    def reset_color(self):
        self.w_root.st_mption_1.setStyleSheet(f'background: red;')
        self.w_root.st_motion_2.setStyleSheet(f'background: red;')
        self.w_root.valve_11.setStyleSheet(f'background: red;')
        self.w_root.valve_12.setStyleSheet(f'background: red;')
        self.w_root.valve_21.setStyleSheet(f'background: red;')
        self.w_root.valve_22.setStyleSheet(f'background: red;')

    def handle(self, address):
        cmd = False
        color = 'red'
        result = self.client.read_coils(address).bits[0]
        if result == False:
            cmd = True
            color = 'green'
        self.client.write_coil(address, cmd)
        return color, result

    def get_pressure(self, address):
        pressure = self.client.read_holding_registers(address, 7)
        pressure = [p for p in pressure.registers]
        text = Utilites.convert_response(pressure)
        return text

    def first_motion_control(self):
        self.handle(260)

    def second_motion_control(self):
        self.handle(261)


    def valve11_control(self):
        self.handle(280)


    def valve12_control(self):
        self.handle(281)

    def valve21_control(self):
        self.handle(282)


    def valve22_control(self):
        self.handle(283)

    def manage_control(self):
        cmd = False
        result = self.client.read_coils(258).bits[0]
        if result == False:
            cmd = True
        self.client.write_coil(258, cmd)

    def stop_cotrol(self):
        self.client.write_coil(258, value=0)
        self.client.write_register(330, value=0)
        self.client.close()

    @QtCore.pyqtSlot()
    def moitor(self):
        now = datetime.datetime.now()
        self.w_root.date.setText(now.strftime('%c'))
        self.w_root.pr_1.setText(self.get_pressure(286))
        self.w_root.pr_2.setText(self.get_pressure(272))
        self.w_root.pr_3.setText(self.get_pressure(300))
        self.w_root.pr_4.setText(self.get_pressure(314))
        manage = Utilites.color(self.client.read_coils(258).bits[0])
        self.w_root.manage.setStyleSheet(f'background: {manage};')
        # word = Utilites.text_manage_control(manage)
        # self.w_root.manage.setText(word)
        c1 = Utilites.color(self.client.read_coils(260).bits[0])
        self.w_root.st_mption_1.setStyleSheet(f'background: {c1};')
        c2 = Utilites.color(self.client.read_coils(261).bits[0])
        self.w_root.st_motion_2.setStyleSheet(f'background: {c2};')
        c3 = Utilites.color(self.client.read_coils(290).bits[0])
        self.w_root.valve_11.setStyleSheet(f'background: {c3};')
        c4 = Utilites.color(self.client.read_coils(291).bits[0])
        self.w_root.valve_12.setStyleSheet(f'background: {c4};')
        c5 = Utilites.color(self.client.read_coils(292).bits[0])
        self.w_root.valve_21.setStyleSheet(f'background: {c5};')
        c6 = Utilites.color(self.client.read_coils(293).bits[0])
        self.w_root.valve_22.setStyleSheet(f'background: {c6};')

    def settings_cotrol(self):
        print('settings_cotrol')


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication([])
    application = SPK()
    application.show()
    sys.exit(app.exec())
