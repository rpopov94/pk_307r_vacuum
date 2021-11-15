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
                pressure = Utilites.get_pressure(self.client, 286)
                self.newTextAndColor.emit(float(pressure))
            else:
                self.newTextAndColor.emit(float(random.random()))
            QtCore.QThread.msleep(1000)


class Graph_One(QDialog):
    data_f = []
    def __init__(self, parent=None):
        super(Graph_One, self).__init__(parent)
        self.setWindowTitle('Graph_1')
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.button = QPushButton('Plot')
        # self.button.clicked.connect(self.plot)
        layout = QVBoxLayout()
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        # layout.addWidget(self.button)
        self.setLayout(layout)

        self.one_thread = QtCore.QThread()
        self.browserHandler = BrowserHandler()
        self.browserHandler.moveToThread(self.one_thread)
        self.browserHandler.newTextAndColor.connect(self.plot)
        self.one_thread.started.connect(self.browserHandler.run)
        self.one_thread.start(QtCore.QThread.LowestPriority)

    @QtCore.pyqtSlot(float)
    def plot(self, data):
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.grid(True)
        self.data_f.append(data)
        ax.plot(self.data_f, '*-')
        self.canvas.draw()
