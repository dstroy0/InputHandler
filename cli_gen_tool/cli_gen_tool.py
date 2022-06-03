##
# @file cli_gen_tool.py
# @author Douglas Quigg (dstroy0 dquigg123@gmail.com)
# @brief InputHandler CLI gen tool
# @version 0.1
# @date 2022-05-28
# @copyright Copyright (c) 2022

# Copyright (C) 2022 Douglas Quigg (dstroy0) <dquigg123@gmail.com>

# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# version 3 as published by the Free Software Foundation.

import sys

import csv   #for learning basic data entry
import json  #dump everything, maybe a dict or a tuple -> json

from PyQt5.QtWidgets import (QApplication, QWidget, QMainWindow, QPushButton, QAction, QHeaderView, QLineEdit, QLabel,
                             QTabWidget, QTableWidget, QTreeWidget, QVBoxLayout, QHBoxLayout)
from PyQt5.QtGui import QPainter, QStandardItemModel, QIcon
from PyQt5.QtCore import Qt
from PyQt5.QtChart import QChart, QChartView, QPieSeries

class ParametersDataEntryForm(QWidget):
    def __init__(self, gen_c_code):
        super().__init__()

        self.items = 0

        self._data = {"Output Enabled":False, "Buffer Size in bytes":0, "Process Name":'_test_', "End of line character(s)":'\r\n'}

        # left side 
        self.tree = QTreeWidget()

        self.layoutRight = QVBoxLayout()

        self.layoutRight.addWidget(gen_c_code)

        self.layout = QHBoxLayout()
        self.layout.addWidget(self.tree, 50)

        self.setLayout(self.layout)

class ProcessDataEntryForm(QWidget):
    def __init__(self, gen_p_code):
        super().__init__()        

        self.items = 0

        self._data = {"Output Enabled":False, "Buffer Size in bytes":0, "Process Name":'_test_', "End of line character(s)":'\r\n'}

        # left side 
        self.table = QTableWidget()
        self.table.setColumnCount(2) 
        self.table.setHorizontalHeaderLabels(('Option', 'Setting'))
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch) # stretch table to window width

        self.layoutRight = QVBoxLayout()

        self.layoutRight.addWidget(gen_p_code)

        self.layout = QHBoxLayout()
        self.layout.addWidget(self.table, 50)

        self.setLayout(self.layout)

class MainWindow(QMainWindow):
        def __init__(self, process_widget, parameters_widget):
            super().__init__()
            self.setWindowTitle('InputHandler CLI gen tool')
            # generate icon and add as resource
            #TODO
            # self.setWindowIcon(QIcon('icon'))
            self.resize(1200,800)

            # File menu
            self.menuBar = self.menuBar()
            self.fileMenu = self.menuBar.addMenu('File')

            # export to csv file action
            exportAction = QAction('Export to CSV', self)
            exportAction.setShortcut('Ctrl+E')
            # exportAction.triggered.connect() #TODO

            # save json db to file action
            #TODO
            # saveJsonAction = QAction('Save file', self)
            # saveJsonAction.setShortcut('Ctrl+S')
            # saveJsonAction.triggered.connect() #TODO

            # open file and load json db action
            #TODO
            # openFileLoadJsonAction = QAction('Open file', self)
            # openFileLoadJsonAction.setShortcut('Ctrl+O')
            # openFileLoadJsonAction.triggered.connect() #TODO

            # exit action
            exitAction = QAction('Exit', self)
            exitAction.setShortcut('Ctrl+Q')
            exitAction.triggered.connect(lambda: app.quit())

            # File menu actions
            # self.fileMenu.addAction(saveJsonAction)
            # self.fileMenu.addAction(openFileLoadJsonAction)
            self.fileMenu.addAction(exportAction)
            self.fileMenu.addAction(exitAction)
            
            # central tab widget
            self.tabWidget = QTabWidget()
            self.tabWidget.addTab(process_widget, "Process Settings")
            self.tabWidget.addTab(parameters_widget, "Command Tree Settings")

            self.setCentralWidget(self.tabWidget)

        def export_to_csv(self, file_name:str):
            try:
                with open(file_name, 'w', newline='') as file:
                    writer = csv.writer(file_name)
                    # writer.writerow(                        
                    # )
                    # TODO
                    print('CSV file exported.')
            except Exception as e:
                print(e)

        #TODO
        # save json db to file function
        def save_json_to_file(self, file_name:str):
            try:
                with open(file_name, 'w', newline='') as file:
                    writer = json.dumps(file_name)
                    print('File saved.')
            except Exception as e:
                print(e)
        
        #TODO
        # load json db from file function
        def load_json_from_file(self, file_name:str):
            try:
                with open(file_name, 'r', newline='') as file:
                    writer = json.loads(file_name)
                    print('File load.')
            except Exception as e:
                print(e)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    gen_c_code = QLabel()
    gen_p_code = QLabel()

    # generate code preview
    # TODO
    gen_p_code.setText('process code preview')
    gen_c_code.setText('parameters code preview')
    
    # objects to pass to MainWindow
    p = ProcessDataEntryForm(gen_p_code)
    c = ParametersDataEntryForm(gen_c_code)    
    cli_gen_tool = MainWindow(p, c)
    cli_gen_tool.show()
    
    sys.exit(app.exec_())