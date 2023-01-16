# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'generateCLIDialog.ui'
##
## Created by: Qt User Interface Compiler version 6.3.2
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QDialog, QDialogButtonBox,
    QFrame, QGridLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QRadioButton, QSizePolicy,
    QVBoxLayout, QWidget)

class Ui_generateDialog(object):
    def setupUi(self, generateDialog):
        if not generateDialog.objectName():
            generateDialog.setObjectName(u"generateDialog")
        generateDialog.resize(402, 178)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(generateDialog.sizePolicy().hasHeightForWidth())
        generateDialog.setSizePolicy(sizePolicy)
        self.verticalLayout = QVBoxLayout(generateDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.frame = QFrame(generateDialog)
        self.frame.setObjectName(u"frame")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy1)
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout = QHBoxLayout(self.frame)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label = QLabel(self.frame)
        self.label.setObjectName(u"label")
        sizePolicy2 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy2)

        self.horizontalLayout.addWidget(self.label)

        self.outputPathLineEdit = QLineEdit(self.frame)
        self.outputPathLineEdit.setObjectName(u"outputPathLineEdit")
        self.outputPathLineEdit.setReadOnly(True)

        self.horizontalLayout.addWidget(self.outputPathLineEdit)

        self.pushButton = QPushButton(self.frame)
        self.pushButton.setObjectName(u"pushButton")

        self.horizontalLayout.addWidget(self.pushButton)


        self.verticalLayout.addWidget(self.frame)

        self.frame_2 = QFrame(generateDialog)
        self.frame_2.setObjectName(u"frame_2")
        sizePolicy3 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.frame_2.sizePolicy().hasHeightForWidth())
        self.frame_2.setSizePolicy(sizePolicy3)
        self.frame_2.setFrameShape(QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.gridLayout = QGridLayout(self.frame_2)
        self.gridLayout.setObjectName(u"gridLayout")
        self.platformioRadioButton = QRadioButton(self.frame_2)
        self.platformioRadioButton.setObjectName(u"platformioRadioButton")
        sizePolicy2.setHeightForWidth(self.platformioRadioButton.sizePolicy().hasHeightForWidth())
        self.platformioRadioButton.setSizePolicy(sizePolicy2)

        self.gridLayout.addWidget(self.platformioRadioButton, 1, 1, 1, 1)

        self.arduinoRadioButton = QRadioButton(self.frame_2)
        self.arduinoRadioButton.setObjectName(u"arduinoRadioButton")
        sizePolicy2.setHeightForWidth(self.arduinoRadioButton.sizePolicy().hasHeightForWidth())
        self.arduinoRadioButton.setSizePolicy(sizePolicy2)

        self.gridLayout.addWidget(self.arduinoRadioButton, 1, 0, 1, 1)

        self.label_2 = QLabel(self.frame_2)
        self.label_2.setObjectName(u"label_2")
        sizePolicy1.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy1)
        self.label_2.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.label_2, 0, 0, 1, 2)


        self.verticalLayout.addWidget(self.frame_2)

        self.buttonBox = QDialogButtonBox(generateDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(True)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(generateDialog)
        self.buttonBox.accepted.connect(generateDialog.accept)
        self.buttonBox.rejected.connect(generateDialog.reject)

        QMetaObject.connectSlotsByName(generateDialog)
    # setupUi

    def retranslateUi(self, generateDialog):
        generateDialog.setWindowTitle(QCoreApplication.translate("generateDialog", u"Generate CLI", None))
        self.label.setText(QCoreApplication.translate("generateDialog", u"Output Path:", None))
        self.pushButton.setText(QCoreApplication.translate("generateDialog", u"Change...", None))
        self.platformioRadioButton.setText(QCoreApplication.translate("generateDialog", u"Platformio", None))
        self.arduinoRadioButton.setText(QCoreApplication.translate("generateDialog", u"Arduino", None))
        self.label_2.setText(QCoreApplication.translate("generateDialog", u"Output File Structure", None))
    # retranslateUi

