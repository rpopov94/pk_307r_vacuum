from graph_one import Graph_One
from graph_second import Graph_Second
from spk_307 import Ui_Dialog
import datetime
from settings_ui import *
import logging
import pandas as pd


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
    now = datetime.now()
    df = pd.DataFrame()
    df.to_csv(f'{now.strftime("%Y-%m-%d")}.csv')
    pressure = QtCore.pyqtSignal(int, int)
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
        self.w_root.pushButton.clicked.connect(self.graph_1)
        self.w_root.pushButton_2.clicked.connect(self.graph_2)
        self.w2 = Graph_One()
        self.w3 = Graph_Second()

        self.thread = QtCore.QThread()
        self.browserHandler = BrowserHandler()
        self.browserHandler.moveToThread(self.thread)
        self.browserHandler.newTextAndColor.connect(self.monitor)
        self.thread.started.connect(self.browserHandler.run)
        self.thread.start(QtCore.QThread.LowestPriority) #раскоментировать когда будет подключена связь

        '''#######################logger ########################'''
        ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        logTextBox = QTextEditLogger(self)
        try:
            self.client = ModbusTcpClient(ip)
            self.client.connect()
        except:
            pass
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
        if self.w3.two_thread.isRunning():
            self.w3.two_thread.quit()
        self.w2.show()

    def graph_2(self):
        if self.w2.one_thread.isRunning():
            self.w2.one_thread.quit()
        self.w3.show()

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


    def get_pressure(self, address):
        pressure = self.client.read_holding_registers(address, 7)
        pressure = [p for p in pressure.registers]
        text = Utilites.convert_response(pressure)
        return text

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

    @QtCore.pyqtSlot()
    def monitor(self):
        try:
            now = datetime.datetime.now()
            self.w_root.date.setText(now.strftime('%c'))
            pressure1 = self.get_pressure(286)
            pressure2 = self.get_pressure(272)
            pressure3 = self.get_pressure(300)
            pressure4 = self.get_pressure(314)
            Utilites.data_save(valve_1 = pressure1, valve_2 = pressure2,
                               valve_3 = pressure3, valve_4 = pressure4)
            self.w_root.pr_1.setText(pressure1)
            self.w_root.pr_2.setText(pressure2)
            self.w_root.pr_3.setText(pressure3)
            self.w_root.pr_4.setText(pressure4)
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
            logging.error('Thread not work!')
            self.w_root.pr_1.setText('None')
            self.w_root.pr_2.setText('None')
            self.w_root.pr_3.setText('None')
            self.w_root.pr_4.setText('None')

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
