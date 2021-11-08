# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
from pymodbus.client.sync import ModbusTcpClient
from settings import ip
import logging


# class Worker(QtCore.QThread):
#     try:
#         client = ModbusTcpClient(ip)
#         client.connect()
#         pump_1 = client.read_holding_registers(10300)
#         pump_2 = client.read_holding_registers(10302)
#         valve_1_max = client.read_holding_registers(10316)
#         valve_2_max = client.read_holding_registers(10318)
#         valve_3_max = client.read_holding_registers(10320)
#         valve_4_max = client.read_holding_registers(10322)
#         valve_1_min = client.read_holding_registers(10308)
#         valve_2_min = client.read_holding_registers(10310)
#         valve_3_min = client.read_holding_registers(10312)
#         valve_4_min = client.read_holding_registers(10314)
#     except:
#         print('ModbusTcpClient connection error')
#
#     def __init__(self):
#         QtCore.QThread.__init__(self)

    # def run(self):
    #     while True:
    #         try:
    #             pump_1 = self.client.read_holding_registers(10300)
    #             pump_2 = self.client.read_holding_registers(10302)
    #             valve_1_max = self.client.read_holding_registers(10316)
    #             valve_2_max = self.client.read_holding_registers(10318)
    #             valve_3_max = self.client.read_holding_registers(10320)
    #             valve_4_max = self.client.read_holding_registers(10322)
    #             valve_1_min = self.client.read_holding_registers(10308)
    #             valve_2_min = self.client.read_holding_registers(10310)
    #             valve_3_min = self.client.read_holding_registers(10312)
    #             valve_4_min = self.client.read_holding_registers(10314)
    #         except:
    #             pump_1 = self.pump_1
    #             pump_2 = self.pump_2
    #             valve_1_max = self.valve_1_max
    #             valve_2_max = self.valve_2_max
    #             valve_3_max = self.valve_3_max
    #             valve_4_max = self.valve_4_max
    #             valve_1_min = self.valve_1_min
    #             valve_2_min = self.valve_2_min
    #             valve_3_min = self.valve_3_min
    #             valve_4_min = self.valve_4_min
    #         QtCore.QThread.msleep(1000)
class SettingsHandler(QtCore.QObject):
    newTextAndColor = QtCore.pyqtSignal()

    def run(self):
        while True:
            self.newTextAndColor.emit()
            QtCore.QThread.msleep(1000)


class Ui_Settings(object):

    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(675, 458)
        self.gridLayoutWidget = QtWidgets.QWidget(Dialog)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(100, 130, 461, 178))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.klapan_2_max = QtWidgets.QTextEdit(self.gridLayoutWidget)
        self.klapan_2_max.setMaximumSize(QtCore.QSize(98, 30))
        self.klapan_2_max.setObjectName("klapan_2_max")
        self.gridLayout.addWidget(self.klapan_2_max, 2, 4, 1, 1)
        self.klapan_1_max = QtWidgets.QTextEdit(self.gridLayoutWidget)
        self.klapan_1_max.setMaximumSize(QtCore.QSize(98, 30))
        self.klapan_1_max.setObjectName("klapan_1_max")
        self.gridLayout.addWidget(self.klapan_1_max, 1, 4, 1, 1)
        self.klapan_2_min = QtWidgets.QTextEdit(self.gridLayoutWidget)
        self.klapan_2_min.setMaximumSize(QtCore.QSize(98, 30))
        self.klapan_2_min.setObjectName("klapan_2_min")
        self.gridLayout.addWidget(self.klapan_2_min, 2, 2, 1, 1)
        self.label = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 2, 1, 1)
        self.klapan_3_max = QtWidgets.QTextEdit(self.gridLayoutWidget)
        self.klapan_3_max.setMaximumSize(QtCore.QSize(98, 30))
        self.klapan_3_max.setObjectName("klapan_3_max")
        self.gridLayout.addWidget(self.klapan_3_max, 3, 4, 1, 1)
        self.klapan_3_min = QtWidgets.QTextEdit(self.gridLayoutWidget)
        self.klapan_3_min.setMaximumSize(QtCore.QSize(98, 30))
        self.klapan_3_min.setObjectName("klapan_3_min")
        self.gridLayout.addWidget(self.klapan_3_min, 3, 2, 1, 1)
        self.klapan_4_min = QtWidgets.QTextEdit(self.gridLayoutWidget)
        self.klapan_4_min.setMaximumSize(QtCore.QSize(98, 30))
        self.klapan_4_min.setObjectName("klapan_4_min")
        self.gridLayout.addWidget(self.klapan_4_min, 4, 2, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 1, 0, 1, 1)
        self.valve_1 = QtWidgets.QTextEdit(self.gridLayoutWidget)
        self.valve_1.setMaximumSize(QtCore.QSize(98, 30))
        self.valve_1.setObjectName("valve_1")
        self.gridLayout.addWidget(self.valve_1, 1, 1, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 2, 0, 1, 1)
        self.valve_2 = QtWidgets.QTextEdit(self.gridLayoutWidget)
        self.valve_2.setMaximumSize(QtCore.QSize(98, 30))
        self.valve_2.setObjectName("valve_2")
        self.gridLayout.addWidget(self.valve_2, 2, 1, 1, 1)
        self.klapan_1_min = QtWidgets.QTextEdit(self.gridLayoutWidget)
        self.klapan_1_min.setMaximumSize(QtCore.QSize(98, 30))
        self.klapan_1_min.setObjectName("klapan_1_min")
        self.gridLayout.addWidget(self.klapan_1_min, 1, 2, 1, 1)
        self.klapan_4_max = QtWidgets.QTextEdit(self.gridLayoutWidget)
        self.klapan_4_max.setMaximumSize(QtCore.QSize(98, 30))
        self.klapan_4_max.setObjectName("klapan_4_max")
        self.gridLayout.addWidget(self.klapan_4_max, 4, 4, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 4, 1, 1)
        self.ip_adress = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.ip_adress.setObjectName("ip_adress")
        self.gridLayout.addWidget(self.ip_adress, 1, 5, 1, 1)
        self.datchicki = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.datchicki.setObjectName("datchicki")
        self.gridLayout.addWidget(self.datchicki, 2, 5, 1, 1)
        self.i_o_manage = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.i_o_manage.setObjectName("i_o_manage")
        self.gridLayout.addWidget(self.i_o_manage, 3, 5, 1, 1)
        self.send = QtWidgets.QPushButton(Dialog)
        self.send.setGeometry(QtCore.QRect(580, 400, 75, 23))
        self.send.setText("OK")
        self.send.setObjectName("send")
        try:
            self.client = ModbusTcpClient(ip)
            self.client.connect()
        except:
            print('ModbusTcpClient connection error')

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        self.ip_adress.clicked.connect(self.ip_address_control)
        self.datchicki.clicked.connect(self.datchicki_control)
        self.i_o_manage.clicked.connect(self.hand_manage)
        self.send.clicked.connect(self.send_settings)

        # self.thread = QtCore.QThread()
        # self.browserHandler = SettingsHandler()
        # self.browserHandler.moveToThread(self.thread)
        # self.browserHandler.newTextAndColor.connect(self.datchicki_control)
        # self.thread.started.connect(self.browserHandler.run)
        # self.thread.start()

    def ip_address_control(self):
        print('ip_adress')

    def datchicki_control(self):
        try:
            self.client.read_holding_registers(10300)
            self.client.read_holding_registers(10302)
            self.client.read_holding_registers(10316)
            self.client.read_holding_registers(10318)
            self.client.read_holding_registers(10320)
            self.client.read_holding_registers(10322)
            self.client.read_holding_registers(10308)
            self.client.read_holding_registers(10310)
            self.client.read_holding_registers(10312)
            self.client.read_holding_registers(10314)
        except:
            pass

    def hand_manage(self):
        print('hand_manage')

    def send_settings(self):
        try:
            self.client.write_registers(10300, int(self.valve_1.toPlainText()))
            self.client.write_registers(10302, int(self.valve_2.toPlainText()))
            self.client.write_registers(10316, int(self.klapan_1_min.toPlainText()))
            self.client.write_registers(10318, int(self.klapan_2_min.toPlainText()))
            self.client.write_registers(10320, int(self.klapan_3_min.toPlainText()))
            self.client.write_registers(10322, int(self.klapan_4_min.toPlainText()))
            self.client.write_registers(10308, int(self.klapan_1_max.toPlainText()))
            self.client.write_registers(10310, int(self.klapan_2_max.toPlainText()))
            self.client.write_registers(10312, int(self.klapan_3_max.toPlainText()))
            self.client.write_registers(10314, int(self.klapan_4_max.toPlainText()))
        except:
            self.valve_1.setText('-1')
            self.valve_2.setText('-1')
            self.klapan_1_min.setText('-1')
            self.klapan_2_min.setText('-1')
            self.klapan_3_min.setText('-1')
            self.klapan_4_min.setText('-1')
            self.klapan_1_max.setText('-1')
            self.klapan_2_max.setText('-1')
            self.klapan_3_max.setText('-1')
            self.klapan_4_max.setText('-1')
            logging.error('Ошибка отправки данных, проверьте свой ввод!')

    def update_values(self):
        print('update_values')

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Settings"))
        self.label.setText(_translate("Dialog", "Min"))
        self.label_3.setText(_translate("Dialog", "Насос 1"))
        self.label_4.setText(_translate("Dialog", "Насос 2"))
        self.label_2.setText(_translate("Dialog", "Max"))
        self.ip_adress.setText(_translate("Dialog", "IP адрес"))
        self.datchicki.setText(_translate("Dialog", "Настройка датчиков"))
        self.i_o_manage.setText(_translate("Dialog", "Ручное управление \n Вход-Выход"))





