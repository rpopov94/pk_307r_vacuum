import pandas as pd
import numpy as np
from spk_307 import Ui_Dialog
from graph import DrawGraph
import datetime
from utilites import Utilites
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
    pressures = QtCore.pyqtSignal(list)

    def __init__(self, client):
        super().__init__()
        self.client = client

    def run(self):
        while True:
            pressure1 = Utilites.get_pressure_for_set_data(286, self.client)
            pressure2 = Utilites.get_pressure_for_set_data(272, self.client)
            pressure3 = Utilites.get_pressure_for_set_data(300, self.client)
            pressure4 = Utilites.get_pressure_for_set_data(314, self.client)

            self.pressures.emit(
                [pressure1, pressure2, pressure3, pressure4]
            )
            QtCore.QThread.msleep(1500)


class SPK(QtWidgets.QWidget):
    pressure = QtCore.pyqtSignal(int, int)

    def __init__(self):
        super().__init__()
        self.w_root = Ui_Dialog()
        self.w_root.setupUi(self)
        self.IP = Utilites.get_ip()
        self.w_root.st_mption_1.clicked.connect(self.first_motion_control)
        self.w_root.st_motion_2.clicked.connect(self.second_motion_control)
        self.w_root.valve_11.clicked.connect(self.valve11_control)
        self.w_root.valve_12.clicked.connect(self.valve12_control)
        self.w_root.valve_21.clicked.connect(self.valve21_control)
        self.w_root.valve_22.clicked.connect(self.valve22_control)
        self.w_root.manage.clicked.connect(self.manage_control)
        self.w_root.stop.clicked.connect(self.stop_cotrol)
        self.w_root.settings.clicked.connect(self.settings_cotrol)
        self.w_root.pushButton.clicked.connect(self.graph_1)
        self.w_root.pushButton_2.clicked.connect(self.graph_2)
        self.client = ModbusTcpClient(self.IP)
        self.client.connect()

        self.thread = QtCore.QThread()
        self.browserHandler = BrowserHandler(self.client)
        self.browserHandler.moveToThread(self.thread)
        self.browserHandler.pressures.connect(self.monitor)
        self.thread.started.connect(self.browserHandler.run)
        self.thread.start(QtCore.QThread.LowestPriority)

        '''#######################logger ########################'''
        ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        logTextBox = QTextEditLogger(self)
        # log to text box
        logTextBox.setFormatter(
            logging.Formatter(
                '%(asctime)s %(levelname)s %(module)s %(funcName)s %(message)s'))
        logging.getLogger().addHandler(logTextBox)
        logging.getLogger().setLevel(logging.DEBUG)

        # log to file
        fh = logging.FileHandler('logfile.log')
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(
            logging.Formatter(
                '%(asctime)s %(levelname)s %(module)s %(funcName)s %(message)s'))
        logging.getLogger().addHandler(fh)

    ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

    def graph_1(self):
        '''
         addess = 286
        '''
        self.w2 = DrawGraph(self.IP, 286)
        self.w2.show()

    def graph_2(self):
        ''''
        addess = 300
        '''
        self.w2 = DrawGraph(self.IP, 300)
        self.w2.show()

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
        self.client.write_coil(address, cmd)

    def first_motion_control(self):
        try:
            self.handle(260)
        except:
            logging.warning('Address 260 not changed')

    def second_motion_control(self):
        try:
            self.handle(261)
        except:
            logging.warning('Address 261 not changed')

    def valve11_control(self):
        try:
            self.handle(280)
        except:
            logging.warning('Address 280 not changed')

    def valve12_control(self):
        try:
            self.handle(281)
        except:
            logging.warning('Address 281 not changed')

    def valve21_control(self):
        try:
            self.handle(282)
        except:
            logging.warning('Address 282 not changed')

    def valve22_control(self):
        self.handle(283)

    def manage_control(self):
        try:
            cmd = False
            result = self.client.read_coils(258).bits[0]
            if result == False:
                cmd = True
            self.client.write_coil(258, cmd)
        except:
            logging.warning('Address 258 not changed')

    def stop_cotrol(self):
        try:
            self.client.write_coil(258, value=0)
            self.client.write_register(330, value=0)
        except:
            logging.warning('Button stop not worked')

    @QtCore.pyqtSlot(list)
    def monitor(self, data):
        now = datetime.datetime.now()
        try:
            self.w_root.date.setText(now.strftime('%c'))
            self.w_root.pr_1.setText(data[0])
            self.w_root.pr_2.setText(data[1])
            self.w_root.pr_3.setText(data[2])
            self.w_root.pr_4.setText(data[3])
            names = ['valve_1', 'valve_2', 'valve_3', 'valve_4']
            f = open(f'{now.strftime("%Y-%m-%d")}.csv', 'a')
            writer = csv.DictWriter(f, fieldnames=names)
            writer.writerow({
                'valve_1':data[0][:-6],
                'valve_2':data[1][:-6],
                'valve_3':data[2][:-6],
                'valve_4':data[3][:-6]
            })
            f.close()
        except:
            logging.error('Thread not work!')
            self.w_root.pr_1.setText('None')
            self.w_root.pr_2.setText('None')
            self.w_root.pr_3.setText('None')
            self.w_root.pr_4.setText('None')
        try:
            self.pressure.emit(int(self.w_root.pr_4.text()), int(self.w_root.pr_1.text()))
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
            pass



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
