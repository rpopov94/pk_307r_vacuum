from spk_307 import Ui_Dialog
from PyQt5 import QtWidgets
from PyQt5 import QtCore
from pymodbus.client.sync import ModbusTcpClient
from settings import ip
from utilites import Utilites


class BrowserHandler(QtCore.QObject):
    running = False
    newTextAndColor = QtCore.pyqtSignal()

    # метод, который будет выполнять алгоритм в другом потоке
    def run(self):
        while True:
            # посылаем сигнал из второго потока в GUI поток
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
        # self.w_root.start_manage.clicked.connect(self.moitor)

        # создадим поток
        self.thread = QtCore.QThread()
        # создадим объект для выполнения кода в другом потоке
        self.browserHandler = BrowserHandler()
        # перенесём объект в другой поток
        self.browserHandler.moveToThread(self.thread)
        # после чего подключим все сигналы и слоты
        self.browserHandler.newTextAndColor.connect(self.moitor)
        # подключим сигнал старта потока к методу run у объекта, который должен выполнять код в другом потоке
        self.thread.started.connect(self.browserHandler.run)
        # запустим поток
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
        # print(result)
        if result == False:
            cmd = True
            color = 'green'
        self.client.write_coil(address, cmd)
        return color

    def get_pressure(self, address):
        '''
        :param address: address for read
        :example: 11831,14134,17714,12843,21536,21071,82
        :return: str
        '''
        pressure = self.client.read_holding_registers(address, 7)
        pressure = [p for p in pressure.registers]
        # print(type(pressure))
        text = Utilites.convert_response(pressure)
        return text

    # @QtCore.pyqtSlot()
    def first_motion_control(self):
        # print('first_motion_control')
        color = self.handle(260)
        self.w_root.st_mption_1.setStyleSheet(f'background: {color};')
        pressure = self.get_pressure(268)
        self.w_root.volume_1_info.setText(pressure)

    def second_motion_control(self):
        # print('second_motion_control')
        # address = 261
        color = self.handle(261)
        self.w_root.st_motion_2.setStyleSheet(f'background: {color};')
        pressure = self.get_pressure(270)
        self.w_root.volume_2_info.setText(pressure)

    def valve11_control(self):
        # print('valve11_control')
        # self.client.write_coil(280, 1)
        color = self.handle(280)
        self.w_root.valve_11.setStyleSheet(f'background: {color};')
        pressure = self.get_pressure(272)
        self.w_root.pr_1.setText(pressure)


    def valve12_control(self):
        # print('valve12_control')
        # self.client.write_coil(281, 1)
        color = self.handle(281)
        self.w_root.valve_12.setStyleSheet(f'background: {color};')
        pressure = self.get_pressure(286)
        self.w_root.pr_2.setText(pressure)

    def valve21_control(self):
        # print('valve21_control')
        # self.client.write_coil(282, 1)
        # address = 282
        color = self.handle(282)
        self.w_root.valve_21.setStyleSheet(f'background: {color};')
        pressure = self.get_pressure(300)
        self.w_root.pr_3.setText(pressure)


    def valve22_control(self):
        # print('valve22_control')
        # self.client.write_coil(283, 1)
        color = self.handle(283)
        self.w_root.valve_22.setStyleSheet(f'background: {color};')
        pressure = self.get_pressure(314)
        self.w_root.pr_4.setText(pressure)

    def manage_control(self):
        # print('manage_control')
        client = ModbusTcpClient(ip)
        client.connect()
        cmd = False
        result = self.client.read_coils(258).bits[0]
        # print(result)
        if result == False:
            cmd = True
        client.write_coil(258, cmd)
        client.close()
        self.reset_color()

    def stop_cotrol(self):
        self.client.write_coil(258, False)
        self.client.write_register(330, value=0)
        self.client.close()

    def button_monitor(self):
        pass

    def moitor(self):
        self.w_root.pr_1.setText(self.get_pressure(272))
        self.w_root.pr_2.setText(self.get_pressure(286))
        self.w_root.volume_1_info.setText(self.get_pressure(268))
        self.w_root.pr_3.setText(self.get_pressure(300))
        self.w_root.pr_4.setText(self.get_pressure(314))
        self.w_root.volume_2_info.setText(self.get_pressure(270))




    def settings_cotrol(self):
        print('settings_cotrol')


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication([])
    application = SPK()
    application.show()
    sys.exit(app.exec())
