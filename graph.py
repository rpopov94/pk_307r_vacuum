import logging
from PyQt5 import QtCore
from PyQt5.QtWidgets import QDialog, QApplication, QPushButton, QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
import random
from pymodbus.client.sync import ModbusTcpClient
from utilites import Utilites


class BrowserHandler(QtCore.QObject):
    
    def __init__(self, ip_address, address):
        super().__init__()
        self.ip_address = ip_address
        self.address = address
        self.client = None

    newTextAndColor = QtCore.pyqtSignal(str)

    def run(self):
        try:
            self.client = ModbusTcpClient(self.ip_address)
        except:
            logging.error('ConnectionError')
        while True:
            if self.client.connect():
                pressure = Utilites.get_pressure(self.client, self.address)
                self.newTextAndColor.emit(str(pressure))
            else:
                self.newTextAndColor.emit(str(random.random()))
            self.client.close()
            QtCore.QThread.msleep(5000)


class DrawGraph(QDialog):

    def __init__(self, ip_address, address, parent=None):
        self.ip_address = ip_address
        self.address = address
        self.data_f = []
        super(DrawGraph, self).__init__(parent)
        self.setWindowTitle('Graph_2')
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.button = QPushButton('Plot')
        layout = QVBoxLayout()
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        self.setLayout(layout)

        self.two_thread = QtCore.QThread()
        self.browserHandler = BrowserHandler(self.ip_address, address)
        self.browserHandler.moveToThread(self.two_thread)
        self.browserHandler.newTextAndColor.connect(self.plot)
        self.two_thread.started.connect(self.browserHandler.run)
        self.two_thread.start(QtCore.QThread.LowestPriority)

    @QtCore.pyqtSlot(str)
    def plot(self, data):
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.grid(True)
        self.data_f.append(float(data[:-6]))
        ax.plot(self.data_f, '*-')
        self.canvas.draw()

