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
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QDialog, QHeaderView, QLabel,
    QLineEdit, QPushButton, QSizePolicy, QTabWidget,
    QTreeView, QTreeWidget, QTreeWidgetItem, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(1200, 800)
        self.widget = QWidget(Dialog)
        self.widget.setObjectName(u"widget")
        self.widget.setGeometry(QRect(0, 0, 1201, 801))
        self.widget.setStyleSheet(u"QWidget#widget{\n"
"background-color:color:rgb(227, 227, 227);}\n"
"")
        self.label_2 = QLabel(self.widget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(320, 10, 511, 21))
        self.label_2.setStyleSheet(u"font: 12pt \"OCR A Extended\";\n"
"color: rgb(0, 0, 0);")
        self.tabWidget = QTabWidget(self.widget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setGeometry(QRect(0, 50, 1201, 771))
        self.lib_settings = QWidget()
        self.lib_settings.setObjectName(u"lib_settings")
        self.tabWidget.addTab(self.lib_settings, "")
        self.command_tree = QWidget()
        self.command_tree.setObjectName(u"command_tree")
        self.addnewcmdbutton = QPushButton(self.command_tree)
        self.addnewcmdbutton.setObjectName(u"addnewcmdbutton")
        self.addnewcmdbutton.setGeometry(QRect(10, 680, 111, 31))
        self.treeWidget = QTreeWidget(self.command_tree)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setText(0, u"1");
        self.treeWidget.setHeaderItem(__qtreewidgetitem)
        self.treeWidget.setObjectName(u"treeWidget")
        self.treeWidget.setGeometry(QRect(110, 110, 256, 192))
        self.treeView = QTreeView(self.command_tree)
        self.treeView.setObjectName(u"treeView")
        self.treeView.setGeometry(QRect(600, 250, 256, 192))
        self.lineEdit = QLineEdit(self.command_tree)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setGeometry(QRect(200, 460, 113, 20))
        self.tabWidget.addTab(self.command_tree, "")

        self.retranslateUi(Dialog)
        self.addnewcmdbutton.clicked.connect(self.treeWidget.clear)

        self.tabWidget.setCurrentIndex(1)


        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.label_2.setText(QCoreApplication.translate("Dialog", u"InputHandler command line interface generation tool", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.lib_settings), QCoreApplication.translate("Dialog", u"Library Settings", None))
        self.addnewcmdbutton.setText(QCoreApplication.translate("Dialog", u"Add New Command", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.command_tree), QCoreApplication.translate("Dialog", u"Command Tree", None))
    # retranslateUi

