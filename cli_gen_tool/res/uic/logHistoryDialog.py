# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'logHistoryDialog.ui'
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
from PySide6.QtWidgets import (QApplication, QDialog, QGridLayout, QPlainTextEdit,
    QSizePolicy, QWidget)

class Ui_logHistoryDialog(object):
    def setupUi(self, logHistoryDialog):
        if not logHistoryDialog.objectName():
            logHistoryDialog.setObjectName(u"logHistoryDialog")
        logHistoryDialog.resize(820, 400)
        sizePolicy = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(logHistoryDialog.sizePolicy().hasHeightForWidth())
        logHistoryDialog.setSizePolicy(sizePolicy)
        logHistoryDialog.setMinimumSize(QSize(820, 400))
        self.gridLayout = QGridLayout(logHistoryDialog)
        self.gridLayout.setObjectName(u"gridLayout")
        self.logHistoryPlainTextEdit = QPlainTextEdit(logHistoryDialog)
        self.logHistoryPlainTextEdit.setObjectName(u"logHistoryPlainTextEdit")
        self.logHistoryPlainTextEdit.setMinimumSize(QSize(800, 0))

        self.gridLayout.addWidget(self.logHistoryPlainTextEdit, 0, 0, 1, 1)


        self.retranslateUi(logHistoryDialog)

        QMetaObject.connectSlotsByName(logHistoryDialog)
    # setupUi

    def retranslateUi(self, logHistoryDialog):
        logHistoryDialog.setWindowTitle(QCoreApplication.translate("logHistoryDialog", u"Session Log History", None))
    # retranslateUi

