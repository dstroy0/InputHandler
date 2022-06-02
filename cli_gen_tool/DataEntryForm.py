import sys
print(sys.path)

import os
path = os.environ['PATH']
print(path)

import csv   #for learning basic data entry
import json  #dump everything, maybe a dict or a tuple -> json

from PyQt5.QtWidgets import (QApplication, QWidget, QMainWindow, QPushButton, QAction, QHeaderView, QLineEdit, QLabel,
                             QTableWidget, QVBoxLayout, QHBoxLayout)
from PyQt5.QtGui import QPainter, QStandardItemModel, QIcon
from PyQt5.QtCore import Qt
from PyQt5.QtChart import QChart, QChartView, QPieSeries

class MainWindow(QMainWindow):
        def __init__(self, widget):
            super().__init__()
            self.setWindowTitle('DataEntryForm')
            #self.setWindowIcon(QIcon(icon path))

if __name__ == '__main__':
    app = QApplication(sys.argv)

    x = ''

    demo = MainWindow(x)
    demo.show()
    
    sys.exit(app.exec_())