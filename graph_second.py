import logging
from PyQt5 import QtCore
from PyQt5.QtWidgets import QDialog, QApplication, QPushButton, QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
import random
from pymodbus.client.sync import ModbusTcpClient
from settings import ip
from utilites import Utilites


class BrowserHandler(QtCore.QObject):
    newTextAndColor = QtCore.pyqtSignal(float)
    try:
        client = ModbusTcpClient(ip)
    except:
        logging.error('ConnectionError')

    def run(self):
        while True:
            if self.client.connect():
                pressure = Utilites.get_pressure(self.client, 300)
                self.newTextAndColor.emit(float(pressure))
            else:
                self.newTextAndColor.emit(float(random.random()))
            QtCore.QThread.msleep(1000)


class Graph_Second(QDialog):
    data_f = []
    def __init__(self, parent=None):
        super(Graph_Second, self).__init__(parent)
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
        self.browserHandler = BrowserHandler()
        self.browserHandler.moveToThread(self.two_thread)
        self.browserHandler.newTextAndColor.connect(self.plot)
        self.two_thread.started.connect(self.browserHandler.run)
        self.two_thread.start(QtCore.QThread.LowestPriority)

    @QtCore.pyqtSlot(float)
    def plot(self, data):
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.grid(True)
        self.data_f.append(data)
        ax.plot(self.data_f, '*-')
        self.canvas.draw()
