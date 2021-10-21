import resources
from PyQt5 import QtCore, QtGui, QtWidgets


class Spk_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(1015, 650)
        self.stop = QtWidgets.QPushButton(Dialog)
        self.stop.setGeometry(QtCore.QRect(820, 320, 75, 71))
        self.stop.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/images/stop.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.stop.setIcon(icon)
        self.stop.setIconSize(QtCore.QSize(128, 128))
        self.stop.setObjectName("stop")
        self.settings = QtWidgets.QPushButton(Dialog)
        self.settings.setGeometry(QtCore.QRect(840, 590, 111, 31))
        self.settings.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/images/settings.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.settings.setIcon(icon1)
        self.settings.setIconSize(QtCore.QSize(128, 64))
        self.settings.setObjectName("settings")
        self.system_1 = QtWidgets.QLabel(Dialog)
        self.system_1.setGeometry(QtCore.QRect(50, 30, 431, 271))
        self.system_1.setText("")
        self.system_1.setPixmap(QtGui.QPixmap(":/images/system.png"))
        self.system_1.setObjectName("system_1")
        self.system_2 = QtWidgets.QLabel(Dialog)
        self.system_2.setGeometry(QtCore.QRect(50, 310, 431, 271))
        self.system_2.setText("")
        self.system_2.setPixmap(QtGui.QPixmap(":/images/system.png"))
        self.system_2.setObjectName("system_2")
        self.volume_1 = QtWidgets.QLabel(Dialog)
        self.volume_1.setGeometry(QtCore.QRect(428, 109, 251, 170))
        self.volume_1.setText("")
        self.volume_1.setPixmap(QtGui.QPixmap(":/images/volume.png"))
        self.volume_1.setObjectName("volume_1")
        self.volume_2 = QtWidgets.QLabel(Dialog)
        self.volume_2.setGeometry(QtCore.QRect(428, 389, 251, 171))
        self.volume_2.setText("")
        self.volume_2.setPixmap(QtGui.QPixmap(":/images/volume.png"))
        self.volume_2.setObjectName("volume_2")
        self.st_mption_1 = QtWidgets.QPushButton(Dialog)
        self.st_mption_1.setGeometry(QtCore.QRect(170, 240, 31, 31))
        self.st_mption_1.setStyleSheet("background: red;\n"
                                        "border-radius: 20px;")
        self.st_mption_1.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/images/diode.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.st_mption_1.setIcon(icon2)
        self.st_mption_1.setIconSize(QtCore.QSize(32, 32))
        self.st_mption_1.setObjectName("st_mption_1")
        self.st_motion_2 = QtWidgets.QPushButton(Dialog)
        self.st_motion_2.setGeometry(QtCore.QRect(170, 510, 30, 30))
        self.st_motion_2.setStyleSheet("background: red;\n"
                                        "border-radius: 20px;")
        self.st_motion_2.setText("")
        self.st_motion_2.setIcon(icon2)
        self.st_motion_2.setIconSize(QtCore.QSize(32, 32))
        self.st_motion_2.setObjectName("st_motion_2")
        self.valve_11 = QtWidgets.QPushButton(Dialog)
        self.valve_11.setGeometry(QtCore.QRect(312, 44, 31, 31))
        self.valve_11.setStyleSheet("background: red;\n"
"")
        self.valve_11.setText("")
        self.valve_11.setIcon(icon2)
        self.valve_11.setIconSize(QtCore.QSize(32, 32))
        self.valve_11.setObjectName("valve_11")
        self.valve_21 = QtWidgets.QPushButton(Dialog)
        self.valve_21.setGeometry(QtCore.QRect(314, 320, 31, 31))
        self.valve_21.setStyleSheet("background: red;\n"
"")
        self.valve_21.setText("")
        self.valve_21.setIcon(icon2)
        self.valve_21.setIconSize(QtCore.QSize(32, 32))
        self.valve_21.setObjectName("valve_21")
        self.valve_22 = QtWidgets.QPushButton(Dialog)
        self.valve_22.setGeometry(QtCore.QRect(312, 468, 31, 31))
        self.valve_22.setStyleSheet("background: red;")
        self.valve_22.setText("")
        self.valve_22.setIcon(icon2)
        self.valve_22.setIconSize(QtCore.QSize(32, 32))
        self.valve_22.setObjectName("valve_22")
        self.valve_12 = QtWidgets.QPushButton(Dialog)
        self.valve_12.setGeometry(QtCore.QRect(312, 190, 31, 31))
        self.valve_12.setStyleSheet("background: red;")
        self.valve_12.setText("")
        self.valve_12.setIcon(icon2)
        self.valve_12.setIconSize(QtCore.QSize(32, 32))
        self.valve_12.setObjectName("valve_12")
        self.manage = QtWidgets.QPushButton(Dialog)
        self.manage.setGeometry(QtCore.QRect(800, 160, 131, 61))
        self.manage.setStyleSheet("background: rgb(85, 170, 0);\n"
                                    "border-radius:10px;")
        self.manage.setObjectName("manage")
        self.volume_1_info = QtWidgets.QLabel(Dialog)
        self.volume_1_info.setGeometry(QtCore.QRect(500, 180, 121, 41))
        self.volume_1_info.setStyleSheet("border-style: solid;\n"
                                            "border-width: 1.5px; \n"
                                            "border-color: black;\n"
                                            "")
        self.volume_1_info.setText("")
        self.volume_1_info.setObjectName("volume_1_info")
        self.volume_2_info = QtWidgets.QLabel(Dialog)
        self.volume_2_info.setGeometry(QtCore.QRect(500, 460, 121, 41))
        self.volume_2_info.setStyleSheet("border-style: solid;\n"
                                        "border-width: 1.5px; \n"
                                        "border-color: black;\n"
                                        "")
        self.volume_2_info.setText("")
        self.volume_2_info.setObjectName("volume_2_info")
        self.date = QtWidgets.QLabel(Dialog)
        self.date.setGeometry(QtCore.QRect(790, 10, 211, 41))
        self.date.setText("")
        self.date.setObjectName("date")
        self.pr_1 = QtWidgets.QLabel(Dialog)
        self.pr_1.setGeometry(QtCore.QRect(350, 40, 110, 31))
        self.pr_1.setStyleSheet("border-style: solid;\n"
"border-width: 1.5px; \n"
"border-color: black;\n"
"")
        self.pr_1.setText("")
        self.pr_1.setObjectName("pr_1")
        self.pr_2 = QtWidgets.QLabel(Dialog)
        self.pr_2.setGeometry(QtCore.QRect(270, 150, 110, 31))
        self.pr_2.setStyleSheet("border-style: solid;\n"
                                "border-width: 1.5px; \n"
                                "border-color: black;\n"
                                "")
        self.pr_2.setText("")
        self.pr_2.setObjectName("pr_2")
        self.pr_3 = QtWidgets.QLabel(Dialog)
        self.pr_3.setGeometry(QtCore.QRect(366, 320, 110, 31))
        self.pr_3.setStyleSheet("border-style: solid;\n"
                                "border-width: 1.5px; \n"
                                "border-color: black;\n"
                                "")
        self.pr_3.setText("")
        self.pr_3.setObjectName("pr_3")
        self.pr_4 = QtWidgets.QLabel(Dialog)
        self.pr_4.setGeometry(QtCore.QRect(273, 431, 110, 33))
        self.pr_4.setStyleSheet("border-style: solid;\n"
                                "border-width: 1.5px; \n"
                                "border-color: black;\n"
                                "")
        self.pr_4.setText("")
        self.pr_4.setObjectName("pr_4")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("SPK307", "SPK307"))
        self.manage.setText(_translate("Dialog", "Auto"))

