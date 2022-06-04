# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main.ui'
##
## Created by: Qt User Interface Compiler version 6.3.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QHeaderView, QLabel, QMainWindow,
    QMenu, QMenuBar, QPushButton, QSizePolicy,
    QStatusBar, QTabWidget, QTableWidget, QTableWidgetItem,
    QTreeView, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1413, 892)
        self.actionOpen = QAction(MainWindow)
        self.actionOpen.setObjectName(u"actionOpen")
        self.actionSave = QAction(MainWindow)
        self.actionSave.setObjectName(u"actionSave")
        self.actionPreferences = QAction(MainWindow)
        self.actionPreferences.setObjectName(u"actionPreferences")
        self.actionInputHandler_Documentation = QAction(MainWindow)
        self.actionInputHandler_Documentation.setObjectName(u"actionInputHandler_Documentation")
        self.actionAbout = QAction(MainWindow)
        self.actionAbout.setObjectName(u"actionAbout")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setGeometry(QRect(0, 0, 1421, 871))
        self.tabWidget.setAutoFillBackground(True)
        self.ih_settings_tab = QWidget()
        self.ih_settings_tab.setObjectName(u"ih_settings_tab")
        self.inputhandler_settings_table = QTableWidget(self.ih_settings_tab)
        if (self.inputhandler_settings_table.columnCount() < 2):
            self.inputhandler_settings_table.setColumnCount(2)
        __qtablewidgetitem = QTableWidgetItem()
        self.inputhandler_settings_table.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.inputhandler_settings_table.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        self.inputhandler_settings_table.setObjectName(u"inputhandler_settings_table")
        self.inputhandler_settings_table.setGeometry(QRect(10, 20, 771, 751))
        self.inputhandler_settings_table.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.inputhandler_settings_table.horizontalHeader().setVisible(True)
        self.inputhandler_settings_table.horizontalHeader().setCascadingSectionResizes(False)
        self.inputhandler_settings_table.horizontalHeader().setMinimumSectionSize(50)
        self.inputhandler_settings_table.horizontalHeader().setDefaultSectionSize(350)
        self.inputhandler_settings_table.horizontalHeader().setStretchLastSection(False)
        self.editButton = QPushButton(self.ih_settings_tab)
        self.editButton.setObjectName(u"editButton")
        self.editButton.setGeometry(QRect(160, 790, 121, 31))
        self.defaultButton = QPushButton(self.ih_settings_tab)
        self.defaultButton.setObjectName(u"defaultButton")
        self.defaultButton.setGeometry(QRect(290, 790, 121, 31))
        self.clearButton = QPushButton(self.ih_settings_tab)
        self.clearButton.setObjectName(u"clearButton")
        self.clearButton.setGeometry(QRect(420, 790, 121, 31))
        self.label = QLabel(self.ih_settings_tab)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(1070, 0, 121, 21))
        self.codePreview_1 = QTreeView(self.ih_settings_tab)
        self.codePreview_1.setObjectName(u"codePreview_1")
        self.codePreview_1.setGeometry(QRect(790, 20, 611, 801))
        self.tabWidget.addTab(self.ih_settings_tab, "")
        self.command_tab = QWidget()
        self.command_tab.setObjectName(u"command_tab")
        self.treeView = QTreeView(self.command_tab)
        self.treeView.setObjectName(u"treeView")
        self.treeView.setGeometry(QRect(0, 0, 791, 781))
        self.label_2 = QLabel(self.command_tab)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(1060, 0, 121, 21))
        self.codePreview_2 = QTreeView(self.command_tab)
        self.codePreview_2.setObjectName(u"codePreview_2")
        self.codePreview_2.setGeometry(QRect(800, 20, 601, 791))
        self.tabWidget.addTab(self.command_tab, "")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1413, 21))
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        self.menuHelp = QMenu(self.menubar)
        self.menuHelp.setObjectName(u"menuHelp")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addAction(self.actionPreferences)
        self.menuHelp.addAction(self.actionInputHandler_Documentation)
        self.menuHelp.addAction(self.actionAbout)

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"InputHandler CLI generation tool", None))
        self.actionOpen.setText(QCoreApplication.translate("MainWindow", u"Open", None))
        self.actionSave.setText(QCoreApplication.translate("MainWindow", u"Save", None))
        self.actionPreferences.setText(QCoreApplication.translate("MainWindow", u"Preferences", None))
        self.actionInputHandler_Documentation.setText(QCoreApplication.translate("MainWindow", u"InputHandler Documentation", None))
        self.actionAbout.setText(QCoreApplication.translate("MainWindow", u"About", None))
        ___qtablewidgetitem = self.inputhandler_settings_table.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("MainWindow", u"Option", None));
        ___qtablewidgetitem1 = self.inputhandler_settings_table.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("MainWindow", u"Setting", None));
        self.editButton.setText(QCoreApplication.translate("MainWindow", u"Edit", None))
        self.defaultButton.setText(QCoreApplication.translate("MainWindow", u"Default", None))
        self.clearButton.setText(QCoreApplication.translate("MainWindow", u"Clear", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Code Preview", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.ih_settings_tab), QCoreApplication.translate("MainWindow", u"InputHandler settings", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Code Preview", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.command_tab), QCoreApplication.translate("MainWindow", u"Command Tree", None))
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
        self.menuHelp.setTitle(QCoreApplication.translate("MainWindow", u"Help", None))
    # retranslateUi

