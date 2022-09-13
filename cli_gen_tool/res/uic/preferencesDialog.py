# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'preferencesDialog.ui'
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QComboBox, QDialog,
    QDialogButtonBox, QGridLayout, QLabel, QLineEdit,
    QPushButton, QSizePolicy, QWidget)

class Ui_Preferences(object):
    def setupUi(self, Preferences):
        if not Preferences.objectName():
            Preferences.setObjectName(u"Preferences")
        Preferences.resize(545, 212)
        self.gridLayout = QGridLayout(Preferences)
        self.gridLayout.setObjectName(u"gridLayout")
        self.label = QLabel(Preferences)
        self.label.setObjectName(u"label")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setMinimumSize(QSize(120, 0))
        self.label.setMaximumSize(QSize(120, 25))
        self.label.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.config_path_input = QLineEdit(Preferences)
        self.config_path_input.setObjectName(u"config_path_input")
        sizePolicy1 = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.config_path_input.sizePolicy().hasHeightForWidth())
        self.config_path_input.setSizePolicy(sizePolicy1)

        self.gridLayout.addWidget(self.config_path_input, 0, 1, 1, 1)

        self.browse_for_config = QPushButton(Preferences)
        self.browse_for_config.setObjectName(u"browse_for_config")

        self.gridLayout.addWidget(self.browse_for_config, 0, 2, 1, 1)

        self.label_2 = QLabel(Preferences)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMaximumSize(QSize(16777215, 25))
        self.label_2.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)

        self.sessionHistoryLogLevelComboBox = QComboBox(Preferences)
        self.sessionHistoryLogLevelComboBox.addItem("")
        self.sessionHistoryLogLevelComboBox.addItem("")
        self.sessionHistoryLogLevelComboBox.addItem("")
        self.sessionHistoryLogLevelComboBox.addItem("")
        self.sessionHistoryLogLevelComboBox.addItem("")
        self.sessionHistoryLogLevelComboBox.setObjectName(u"sessionHistoryLogLevelComboBox")

        self.gridLayout.addWidget(self.sessionHistoryLogLevelComboBox, 1, 1, 1, 1)

        self.label_3 = QLabel(Preferences)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setMaximumSize(QSize(16777215, 25))
        self.label_3.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)

        self.fileLogLevelComboBox = QComboBox(Preferences)
        self.fileLogLevelComboBox.addItem("")
        self.fileLogLevelComboBox.addItem("")
        self.fileLogLevelComboBox.addItem("")
        self.fileLogLevelComboBox.addItem("")
        self.fileLogLevelComboBox.addItem("")
        self.fileLogLevelComboBox.setObjectName(u"fileLogLevelComboBox")

        self.gridLayout.addWidget(self.fileLogLevelComboBox, 2, 1, 1, 1)

        self.label_4 = QLabel(Preferences)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setMaximumSize(QSize(16777215, 25))
        self.label_4.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.label_4, 3, 0, 1, 1)

        self.streamLogLevelComboBox = QComboBox(Preferences)
        self.streamLogLevelComboBox.addItem("")
        self.streamLogLevelComboBox.addItem("")
        self.streamLogLevelComboBox.addItem("")
        self.streamLogLevelComboBox.addItem("")
        self.streamLogLevelComboBox.addItem("")
        self.streamLogLevelComboBox.setObjectName(u"streamLogLevelComboBox")

        self.gridLayout.addWidget(self.streamLogLevelComboBox, 3, 1, 1, 1)

        self.label_5 = QLabel(Preferences)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setMaximumSize(QSize(16777215, 25))
        self.label_5.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.label_5, 4, 0, 1, 1)

        self.globalLogLevelComboBox = QComboBox(Preferences)
        self.globalLogLevelComboBox.addItem("")
        self.globalLogLevelComboBox.addItem("")
        self.globalLogLevelComboBox.addItem("")
        self.globalLogLevelComboBox.addItem("")
        self.globalLogLevelComboBox.addItem("")
        self.globalLogLevelComboBox.setObjectName(u"globalLogLevelComboBox")

        self.gridLayout.addWidget(self.globalLogLevelComboBox, 4, 1, 1, 1)

        self.buttonBox = QDialogButtonBox(Preferences)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setMinimumSize(QSize(0, 25))
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(True)

        self.gridLayout.addWidget(self.buttonBox, 5, 0, 1, 3)


        self.retranslateUi(Preferences)
        self.buttonBox.accepted.connect(Preferences.accept)
        self.buttonBox.rejected.connect(Preferences.reject)

        self.sessionHistoryLogLevelComboBox.setCurrentIndex(0)
        self.fileLogLevelComboBox.setCurrentIndex(0)
        self.streamLogLevelComboBox.setCurrentIndex(0)
        self.globalLogLevelComboBox.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(Preferences)
    # setupUi

    def retranslateUi(self, Preferences):
        Preferences.setWindowTitle(QCoreApplication.translate("Preferences", u"Preferences", None))
        self.label.setText(QCoreApplication.translate("Preferences", u"Input Config File Path", None))
        self.browse_for_config.setText(QCoreApplication.translate("Preferences", u"Browse...", None))
        self.label_2.setText(QCoreApplication.translate("Preferences", u"Session history log level", None))
        self.sessionHistoryLogLevelComboBox.setItemText(0, QCoreApplication.translate("Preferences", u"DEBUG", u"10"))
        self.sessionHistoryLogLevelComboBox.setItemText(1, QCoreApplication.translate("Preferences", u"INFO", u"20"))
        self.sessionHistoryLogLevelComboBox.setItemText(2, QCoreApplication.translate("Preferences", u"WARNING", u"30"))
        self.sessionHistoryLogLevelComboBox.setItemText(3, QCoreApplication.translate("Preferences", u"ERROR", u"40"))
        self.sessionHistoryLogLevelComboBox.setItemText(4, QCoreApplication.translate("Preferences", u"CRITICAL", u"50"))

        self.sessionHistoryLogLevelComboBox.setCurrentText(QCoreApplication.translate("Preferences", u"DEBUG", None))
        self.label_3.setText(QCoreApplication.translate("Preferences", u"File log level", None))
        self.fileLogLevelComboBox.setItemText(0, QCoreApplication.translate("Preferences", u"DEBUG", u"10"))
        self.fileLogLevelComboBox.setItemText(1, QCoreApplication.translate("Preferences", u"INFO", u"20"))
        self.fileLogLevelComboBox.setItemText(2, QCoreApplication.translate("Preferences", u"WARNING", u"30"))
        self.fileLogLevelComboBox.setItemText(3, QCoreApplication.translate("Preferences", u"ERROR", u"40"))
        self.fileLogLevelComboBox.setItemText(4, QCoreApplication.translate("Preferences", u"CRITICAL", u"50"))

        self.fileLogLevelComboBox.setCurrentText(QCoreApplication.translate("Preferences", u"DEBUG", None))
        self.label_4.setText(QCoreApplication.translate("Preferences", u"Stream log level", None))
        self.streamLogLevelComboBox.setItemText(0, QCoreApplication.translate("Preferences", u"DEBUG", u"10"))
        self.streamLogLevelComboBox.setItemText(1, QCoreApplication.translate("Preferences", u"INFO", u"20"))
        self.streamLogLevelComboBox.setItemText(2, QCoreApplication.translate("Preferences", u"WARNING", u"30"))
        self.streamLogLevelComboBox.setItemText(3, QCoreApplication.translate("Preferences", u"ERROR", u"40"))
        self.streamLogLevelComboBox.setItemText(4, QCoreApplication.translate("Preferences", u"CRITICAL", u"50"))

        self.streamLogLevelComboBox.setCurrentText(QCoreApplication.translate("Preferences", u"DEBUG", None))
        self.label_5.setText(QCoreApplication.translate("Preferences", u"Global log level", None))
        self.globalLogLevelComboBox.setItemText(0, QCoreApplication.translate("Preferences", u"DEBUG", u"10"))
        self.globalLogLevelComboBox.setItemText(1, QCoreApplication.translate("Preferences", u"INFO", u"20"))
        self.globalLogLevelComboBox.setItemText(2, QCoreApplication.translate("Preferences", u"WARNING", u"30"))
        self.globalLogLevelComboBox.setItemText(3, QCoreApplication.translate("Preferences", u"ERROR", u"40"))
        self.globalLogLevelComboBox.setItemText(4, QCoreApplication.translate("Preferences", u"CRITICAL", u"50"))

        self.globalLogLevelComboBox.setCurrentText(QCoreApplication.translate("Preferences", u"DEBUG", None))
    # retranslateUi

