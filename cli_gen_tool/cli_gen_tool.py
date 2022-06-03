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
            #self.setWindowIcon(QIcon(icon path))
            self.resize(1200,800)

            self.menuBar = self.menuBar()
            self.fileMenu = self.menuBar.addMenu('File')

            # export to csv file action
            exportAction = QAction('Export to CSV', self)
            exportAction.setShortcut('Ctrl+E')
            # exportAction.triggered.connect() #TODO

            # exit action
            exitAction = QAction('Exit', self)
            exitAction.setShortcut('Ctrl+Q')
            exitAction.triggered.connect(lambda: app.quit())

            self.fileMenu.addAction(exportAction)
            self.fileMenu.addAction(exitAction)
            
            self.tabWidget = QTabWidget()
            self.tabWidget.addTab(process_widget, "")
            self.tabWidget.addTab(parameters_widget, "")

            self.setCentralWidget(self.tabWidget) #TODO

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



if __name__ == '__main__':
    app = QApplication(sys.argv)
    gen_c_code = QLabel()
    gen_p_code = QLabel()
    # generate code preview
    # TODO
    gen_p_code.setText('process code preview')
    gen_c_code.setText('parameters code preview')
    p = ProcessDataEntryForm(gen_c_code)
    c = ParametersDataEntryForm(gen_p_code)    
    cli_gen_tool = MainWindow(p, c)
    cli_gen_tool.show()
    
    sys.exit(app.exec_())