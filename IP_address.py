# -*- coding: utf-8 -*-
import logging
from PyQt5 import QtCore, QtGui, QtWidgets
from pymodbus.client.sync import ModbusTcpClient
from utilites import *


class Ip_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(382, 373)
        self.gridLayoutWidget = QtWidgets.QWidget(Dialog)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(30, 40, 311, 231))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.plainTextEdit_2 = QtWidgets.QPlainTextEdit(self.gridLayoutWidget)
        self.plainTextEdit_2.setMaximumSize(QtCore.QSize(16777215, 35))
        self.plainTextEdit_2.setObjectName("plainTextEdit_2")
        self.gridLayout.addWidget(self.plainTextEdit_2, 1, 1, 1, 1)
        self.plainTextEdit = QtWidgets.QPlainTextEdit(self.gridLayoutWidget)
        self.plainTextEdit.setMaximumSize(QtCore.QSize(16777215, 35))
        self.plainTextEdit.setObjectName("plainTextEdit")
        self.gridLayout.addWidget(self.plainTextEdit, 0, 1, 1, 1)
        self.plainTextEdit_3 = QtWidgets.QPlainTextEdit(self.gridLayoutWidget)
        self.plainTextEdit_3.setMaximumSize(QtCore.QSize(16777215, 35))
        self.plainTextEdit_3.setObjectName("plainTextEdit_3")
        self.gridLayout.addWidget(self.plainTextEdit_3, 2, 1, 1, 1)
        self.label = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(270, 290, 75, 23))
        self.pushButton.setObjectName("pushButton")
        self.ip = Utilites.get_ip()
        # try:
        #     self.client = ModbusTcpClient(self.ip)
        #     self.client.connect()
        # except:
        #     pass
        # try:
        #     self.plainTextEdit.appendPlainText(str(Utilites.get_values_from_response(self.client.read_holding_registers(10084, 4))))
        #     self.plainTextEdit_2.appendPlainText(str(Utilites.get_values_from_response(self.client.read_holding_registers(10088, 4))))
        #     self.plainTextEdit_3.appendPlainText(str(Utilites.get_values_from_response(self.client.read_holding_registers(10092, 4))))
        # except:
        #     pass
        self.pushButton.clicked.connect(self.send)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def send(self):
        try:
            ip_data = self.plainTextEdit.toPlainText()
            mask_data = self.plainTextEdit_2.toPlainText()
            gateway = self.plainTextEdit_3.toPlainText()
            with open('.env', 'w') as settings:
                settings.write(f'IP={ip_data}')
                settings.close()
            # self.client.write_registers(10084, [int(v) for v in ip_data.split('.')])
            # self.client.write_registers(10088, [int(v) for v in mask_data.split('.')])
            # self.client.write_registers(10092, [int(v) for v in gateway.split('.')])
        except:
            logging.error('Please see you data!')

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "IP address"))
        self.label.setText(_translate("Dialog", "IP"))
        self.label_2.setText(_translate("Dialog", "Маска "))
        self.label_3.setText(_translate("Dialog", "Шлюз"))
        self.pushButton.setText(_translate("Dialog", "BACK"))
