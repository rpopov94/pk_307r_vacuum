from PyQt5.QtWidgets import QMessageBox
from spk_307 import Ui_Dialog
from PyQt5 import QtWidgets
from PyQt5 import QtCore
from pymodbus.client.sync import ModbusTcpClient
from settings import ip
from utilites import Utilites
import datetime
from settings_ui import *
import logging


class QTextEditLogger(logging.Handler, QtCore.QObject):
    appendPlainText = QtCore.pyqtSignal(str)

    def __init__(self, parent):
        super().__init__()
        QtCore.QObject.__init__(self)
        self.widget = QtWidgets.QPlainTextEdit(parent)
        self.widget.setGeometry(QtCore.QRect(0, 0, 300, 100))
        self.widget.setReadOnly(True)
        self.appendPlainText.connect(self.widget.appendPlainText)

    def emit(self, record):
        msg = self.format(record)
        self.appendPlainText.emit(msg)


class BrowserHandler(QtCore.QObject):
    newTextAndColor = QtCore.pyqtSignal()

    def run(self):
        while True:
            self.newTextAndColor.emit()
            QtCore.QThread.msleep(1000)


class SPK(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.w_root = Ui_Dialog()
        self.w_root.setupUi(self)
        self.w_root.st_mption_1.clicked.connect(self.first_motion_control)
        self.w_root.st_motion_2.clicked.connect(self.second_motion_control)
        self.w_root.valve_11.clicked.connect(self.valve11_control)
        self.w_root.valve_12.clicked.connect(self.valve12_control)
        self.w_root.valve_21.clicked.connect(self.valve21_control)
        self.w_root.valve_22.clicked.connect(self.valve22_control)
        self.w_root.manage.clicked.connect(self.manage_control)
        self.w_root.stop.clicked.connect(self.stop_cotrol)
        self.w_root.settings.clicked.connect(self.settings_cotrol)
        logTextBox = QTextEditLogger(self)
        try:
            self.client = ModbusTcpClient(ip)
            self.client.connect()
        except:
            print('ModbusTcpClient connection error')
          # log to text box
        logTextBox.setFormatter(
            logging.Formatter(
                '%(asctime)s %(levelname)s %(module)s %(funcName)s %(message)s'))
        logging.getLogger().addHandler(logTextBox)
        logging.getLogger().setLevel(logging.DEBUG)

        # log to file
        fh = logging.FileHandler('my-log.log')
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(
            logging.Formatter(
                '%(asctime)s %(levelname)s %(module)s %(funcName)s %(message)s'))
        logging.getLogger().addHandler(fh)

        # self.thread = QtCore.QThread()
        # self.browserHandler = BrowserHandler()
        # self.browserHandler.moveToThread(self.thread)
        # self.browserHandler.newTextAndColor.connect(self.monitor)
        # self.thread.started.connect(self.browserHandler.run)
        # self.thread.start()

    def create_logger(path, widget: QtWidgets.QTextEdit):
        log = logging.getLogger('main')
        log.setLevel(logging.DEBUG)

        file_formatter = logging.Formatter(
            ('#%(levelname)-s, %(pathname)s, line %(lineno)d, [%(asctime)s]: '
             '%(message)s'), datefmt='%Y-%m-%d %H:%M:%S'
        )
        console_formatter = logging.Formatter(('#%(levelname)-s, %(pathname)s, '
                                               'line %(lineno)d: %(message)s'))

        log_window_formatter = logging.Formatter(
            '#%(levelname)-s, %(message)s\n'
        )

        file_handler = logging.FileHandler(path)
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(file_formatter)

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(console_formatter)
        console_handler.setLevel(logging.DEBUG)
        console_handler.setFormatter(console_formatter)

        log_window_handler = logging.Handler()
        log_window_handler.emit = lambda record: widget.insertPlainText(
            log_window_handler.format(record)
        )
        log_window_handler.setLevel(logging.DEBUG)
        log_window_handler.setFormatter(log_window_formatter)

        log.addHandler(file_handler)
        log.addHandler(console_handler)
        log.addHandler(log_window_handler)

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

    @QtCore.pyqtSlot()
    def monitor(self):
        try:
            now = datetime.datetime.now()
            self.w_root.date.setText(now.strftime('%c'))
            self.w_root.pr_1.setText(self.get_pressure(286))
            self.w_root.pr_2.setText(self.get_pressure(272))
            self.w_root.pr_3.setText(self.get_pressure(300))
            self.w_root.pr_4.setText(self.get_pressure(314))
            manage = Utilites.color(self.client.read_coils(258).bits[0])
            self.w_root.manage.setStyleSheet(f'background: {manage};')
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
        except:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Error")
            msg.setInformativeText('More information')
            msg.setWindowTitle("Error")
            msg.exec_()

    def settings_cotrol(self):
        self.dialog = QtWidgets.QMainWindow()
        self.ui = Ui_Settings()
        self.ui.setupUi(self.dialog)
        self.dialog.show()

if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication([])
    application = SPK()
    application.show()
    sys.exit(app.exec())
