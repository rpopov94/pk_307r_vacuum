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
    newTextAndColor = QtCore.pyqtSignal(list)
    try:
        client = ModbusTcpClient(ip)
    except:
        logging.error('ConnectionError')
    def run(self):
        while True:
            if self.client.connect():
                list = None
                pressure = Utilites.get_pressure(self.client, 286)
                self.newTextAndColor.emit(pressure)
            else:
                str = None
                self.newTextAndColor.emit([random.random() for i in range(10)])
            QtCore.QThread.msleep(1000)


class Graph_Second(QDialog):
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

    @QtCore.pyqtSlot(list)
    def plot(self, data):
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.grid(True)
        data_f = ['%f' % x for x in data]
        if len(data_f) >= 100:
            data_f.pop(data_f[0])
        ax.plot(data_f, '*-')
        self.canvas.draw()
