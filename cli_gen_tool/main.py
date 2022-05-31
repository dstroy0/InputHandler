import sys
print(sys.path + "\n")

import os
path = os.environ['PATH']
print(path + "\n")

from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QWidget
