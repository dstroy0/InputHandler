# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'commandParametersDialog.ui'
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QCheckBox, QComboBox,
    QDialog, QDialogButtonBox, QGridLayout, QLabel,
    QLineEdit, QPlainTextEdit, QPushButton, QSizePolicy,
    QSpinBox, QWidget)

class Ui_commandParametersDialog(object):
    def setupUi(self, commandParametersDialog):
        if not commandParametersDialog.objectName():
            commandParametersDialog.setObjectName(u"commandParametersDialog")
        commandParametersDialog.resize(724, 371)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(commandParametersDialog.sizePolicy().hasHeightForWidth())
        commandParametersDialog.setSizePolicy(sizePolicy)
        self.gridLayout = QGridLayout(commandParametersDialog)
        self.gridLayout.setObjectName(u"gridLayout")
        self.parametersPane = QWidget(commandParametersDialog)
        self.parametersPane.setObjectName(u"parametersPane")
        self.parametersPane.setMinimumSize(QSize(300, 0))
        self.parametersPane.setMaximumSize(QSize(350, 16777215))
        self.gridLayout_3 = QGridLayout(self.parametersPane)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.label_11 = QLabel(self.parametersPane)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setMinimumSize(QSize(100, 20))
        self.label_11.setMaximumSize(QSize(100, 20))
        self.label_11.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_3.addWidget(self.label_11, 0, 0, 1, 1)

        self.commandString = QLineEdit(self.parametersPane)
        self.commandString.setObjectName(u"commandString")
        self.commandString.setMinimumSize(QSize(0, 20))
        self.commandString.setMaximumSize(QSize(250, 20))

        self.gridLayout_3.addWidget(self.commandString, 0, 1, 1, 1)

        self.label_13 = QLabel(self.parametersPane)
        self.label_13.setObjectName(u"label_13")
        self.label_13.setMinimumSize(QSize(100, 20))
        self.label_13.setMaximumSize(QSize(100, 20))
        self.label_13.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_3.addWidget(self.label_13, 1, 0, 1, 1)

        self.commandLengthLabel = QLabel(self.parametersPane)
        self.commandLengthLabel.setObjectName(u"commandLengthLabel")
        self.commandLengthLabel.setMinimumSize(QSize(0, 20))
        self.commandLengthLabel.setMaximumSize(QSize(100, 20))

        self.gridLayout_3.addWidget(self.commandLengthLabel, 1, 1, 1, 1)

        self.label_15 = QLabel(self.parametersPane)
        self.label_15.setObjectName(u"label_15")
        self.label_15.setMinimumSize(QSize(100, 20))
        self.label_15.setMaximumSize(QSize(100, 20))
        self.label_15.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_3.addWidget(self.label_15, 2, 0, 1, 1)

        self.commandParentId = QLineEdit(self.parametersPane)
        self.commandParentId.setObjectName(u"commandParentId")
        self.commandParentId.setMinimumSize(QSize(0, 20))
        self.commandParentId.setMaximumSize(QSize(250, 20))

        self.gridLayout_3.addWidget(self.commandParentId, 2, 1, 1, 1)

        self.label_14 = QLabel(self.parametersPane)
        self.label_14.setObjectName(u"label_14")
        self.label_14.setMinimumSize(QSize(100, 20))
        self.label_14.setMaximumSize(QSize(100, 20))
        self.label_14.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_3.addWidget(self.label_14, 3, 0, 1, 1)

        self.commandId = QLineEdit(self.parametersPane)
        self.commandId.setObjectName(u"commandId")
        self.commandId.setMaximumSize(QSize(250, 20))

        self.gridLayout_3.addWidget(self.commandId, 3, 1, 1, 1)

        self.commandHasWildcards = QCheckBox(self.parametersPane)
        self.commandHasWildcards.setObjectName(u"commandHasWildcards")

        self.gridLayout_3.addWidget(self.commandHasWildcards, 4, 1, 1, 1)

        self.label_12 = QLabel(self.parametersPane)
        self.label_12.setObjectName(u"label_12")
        self.label_12.setMinimumSize(QSize(100, 0))
        self.label_12.setMaximumSize(QSize(100, 20))
        self.label_12.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_3.addWidget(self.label_12, 5, 0, 1, 1)

        self.commandDepth = QSpinBox(self.parametersPane)
        self.commandDepth.setObjectName(u"commandDepth")

        self.gridLayout_3.addWidget(self.commandDepth, 5, 1, 1, 1)

        self.commandSubcommands_label = QLabel(self.parametersPane)
        self.commandSubcommands_label.setObjectName(u"commandSubcommands_label")
        self.commandSubcommands_label.setMinimumSize(QSize(100, 0))
        self.commandSubcommands_label.setMaximumSize(QSize(90, 20))
        self.commandSubcommands_label.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_3.addWidget(self.commandSubcommands_label, 6, 0, 1, 1)

        self.commandSubcommands = QSpinBox(self.parametersPane)
        self.commandSubcommands.setObjectName(u"commandSubcommands")

        self.gridLayout_3.addWidget(self.commandSubcommands, 6, 1, 1, 1)

        self.label_16 = QLabel(self.parametersPane)
        self.label_16.setObjectName(u"label_16")
        self.label_16.setMinimumSize(QSize(100, 0))
        self.label_16.setMaximumSize(QSize(90, 20))
        self.label_16.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_3.addWidget(self.label_16, 7, 0, 1, 1)

        self.commandArgumentHandling = QComboBox(self.parametersPane)
        self.commandArgumentHandling.addItem("")
        self.commandArgumentHandling.addItem("")
        self.commandArgumentHandling.addItem("")
        self.commandArgumentHandling.setObjectName(u"commandArgumentHandling")

        self.gridLayout_3.addWidget(self.commandArgumentHandling, 7, 1, 1, 1)

        self.buttonBox = QDialogButtonBox(self.parametersPane)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Close|QDialogButtonBox.Ok|QDialogButtonBox.Reset)
        self.buttonBox.setCenterButtons(True)

        self.gridLayout_3.addWidget(self.buttonBox, 8, 0, 1, 2)


        self.gridLayout.addWidget(self.parametersPane, 0, 0, 1, 1)

        self.argumentsPane = QWidget(commandParametersDialog)
        self.argumentsPane.setObjectName(u"argumentsPane")
        self.argumentsPane.setMinimumSize(QSize(375, 310))
        self.argumentsPane.setMaximumSize(QSize(400, 406))
        self.gridLayout_2 = QGridLayout(self.argumentsPane)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.label_9 = QLabel(self.argumentsPane)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setMinimumSize(QSize(70, 25))
        self.label_9.setMaximumSize(QSize(75, 25))
        self.label_9.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_2.addWidget(self.label_9, 0, 0, 1, 1)

        self.commandMinArgs = QSpinBox(self.argumentsPane)
        self.commandMinArgs.setObjectName(u"commandMinArgs")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.commandMinArgs.sizePolicy().hasHeightForWidth())
        self.commandMinArgs.setSizePolicy(sizePolicy1)
        self.commandMinArgs.setMinimumSize(QSize(0, 25))
        self.commandMinArgs.setMaximumSize(QSize(55, 25))

        self.gridLayout_2.addWidget(self.commandMinArgs, 0, 1, 1, 2)

        self.argumentsPlainTextCSV = QPlainTextEdit(self.argumentsPane)
        self.argumentsPlainTextCSV.setObjectName(u"argumentsPlainTextCSV")
        self.argumentsPlainTextCSV.setMinimumSize(QSize(0, 250))
        self.argumentsPlainTextCSV.setMaximumSize(QSize(16777215, 320))
        self.argumentsPlainTextCSV.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)

        self.gridLayout_2.addWidget(self.argumentsPlainTextCSV, 0, 3, 10, 1)

        self.commandMaxArgsLabel = QLabel(self.argumentsPane)
        self.commandMaxArgsLabel.setObjectName(u"commandMaxArgsLabel")
        self.commandMaxArgsLabel.setMinimumSize(QSize(70, 25))
        self.commandMaxArgsLabel.setMaximumSize(QSize(75, 25))
        self.commandMaxArgsLabel.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_2.addWidget(self.commandMaxArgsLabel, 1, 0, 1, 1)

        self.commandMaxArgs = QSpinBox(self.argumentsPane)
        self.commandMaxArgs.setObjectName(u"commandMaxArgs")
        sizePolicy1.setHeightForWidth(self.commandMaxArgs.sizePolicy().hasHeightForWidth())
        self.commandMaxArgs.setSizePolicy(sizePolicy1)
        self.commandMaxArgs.setMinimumSize(QSize(0, 25))
        self.commandMaxArgs.setMaximumSize(QSize(55, 25))

        self.gridLayout_2.addWidget(self.commandMaxArgs, 1, 1, 1, 2)

        self.label = QLabel(self.argumentsPane)
        self.label.setObjectName(u"label")
        sizePolicy2 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy2)
        self.label.setMinimumSize(QSize(70, 25))
        self.label.setMaximumSize(QSize(75, 25))
        self.label.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_2.addWidget(self.label, 2, 0, 1, 1)

        self.add8bituint = QPushButton(self.argumentsPane)
        self.add8bituint.setObjectName(u"add8bituint")
        sizePolicy.setHeightForWidth(self.add8bituint.sizePolicy().hasHeightForWidth())
        self.add8bituint.setSizePolicy(sizePolicy)
        self.add8bituint.setMinimumSize(QSize(25, 25))
        self.add8bituint.setMaximumSize(QSize(25, 25))

        self.gridLayout_2.addWidget(self.add8bituint, 2, 1, 1, 1)

        self.rem = QPushButton(self.argumentsPane)
        self.rem.setObjectName(u"rem")
        sizePolicy.setHeightForWidth(self.rem.sizePolicy().hasHeightForWidth())
        self.rem.setSizePolicy(sizePolicy)
        self.rem.setMinimumSize(QSize(25, 25))
        self.rem.setMaximumSize(QSize(25, 25))

        self.gridLayout_2.addWidget(self.rem, 2, 2, 1, 1)

        self.label_3 = QLabel(self.argumentsPane)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setMinimumSize(QSize(70, 25))
        self.label_3.setMaximumSize(QSize(75, 25))
        self.label_3.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_2.addWidget(self.label_3, 3, 0, 1, 1)

        self.add16bituint = QPushButton(self.argumentsPane)
        self.add16bituint.setObjectName(u"add16bituint")
        sizePolicy.setHeightForWidth(self.add16bituint.sizePolicy().hasHeightForWidth())
        self.add16bituint.setSizePolicy(sizePolicy)
        self.add16bituint.setMinimumSize(QSize(25, 25))
        self.add16bituint.setMaximumSize(QSize(25, 25))

        self.gridLayout_2.addWidget(self.add16bituint, 3, 1, 1, 1)

        self.rem1 = QPushButton(self.argumentsPane)
        self.rem1.setObjectName(u"rem1")
        sizePolicy.setHeightForWidth(self.rem1.sizePolicy().hasHeightForWidth())
        self.rem1.setSizePolicy(sizePolicy)
        self.rem1.setMinimumSize(QSize(25, 25))
        self.rem1.setMaximumSize(QSize(25, 25))

        self.gridLayout_2.addWidget(self.rem1, 3, 2, 1, 1)

        self.label_2 = QLabel(self.argumentsPane)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMinimumSize(QSize(70, 25))
        self.label_2.setMaximumSize(QSize(75, 25))
        self.label_2.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_2.addWidget(self.label_2, 4, 0, 1, 1)

        self.add32bituint = QPushButton(self.argumentsPane)
        self.add32bituint.setObjectName(u"add32bituint")
        sizePolicy.setHeightForWidth(self.add32bituint.sizePolicy().hasHeightForWidth())
        self.add32bituint.setSizePolicy(sizePolicy)
        self.add32bituint.setMinimumSize(QSize(25, 25))
        self.add32bituint.setMaximumSize(QSize(25, 25))

        self.gridLayout_2.addWidget(self.add32bituint, 4, 1, 1, 1)

        self.rem2 = QPushButton(self.argumentsPane)
        self.rem2.setObjectName(u"rem2")
        sizePolicy.setHeightForWidth(self.rem2.sizePolicy().hasHeightForWidth())
        self.rem2.setSizePolicy(sizePolicy)
        self.rem2.setMinimumSize(QSize(25, 25))
        self.rem2.setMaximumSize(QSize(25, 25))

        self.gridLayout_2.addWidget(self.rem2, 4, 2, 1, 1)

        self.label_4 = QLabel(self.argumentsPane)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setMinimumSize(QSize(70, 25))
        self.label_4.setMaximumSize(QSize(75, 25))
        self.label_4.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_2.addWidget(self.label_4, 5, 0, 1, 1)

        self.add16bitint = QPushButton(self.argumentsPane)
        self.add16bitint.setObjectName(u"add16bitint")
        sizePolicy.setHeightForWidth(self.add16bitint.sizePolicy().hasHeightForWidth())
        self.add16bitint.setSizePolicy(sizePolicy)
        self.add16bitint.setMinimumSize(QSize(25, 25))
        self.add16bitint.setMaximumSize(QSize(25, 25))

        self.gridLayout_2.addWidget(self.add16bitint, 5, 1, 1, 1)

        self.rem3 = QPushButton(self.argumentsPane)
        self.rem3.setObjectName(u"rem3")
        sizePolicy.setHeightForWidth(self.rem3.sizePolicy().hasHeightForWidth())
        self.rem3.setSizePolicy(sizePolicy)
        self.rem3.setMinimumSize(QSize(25, 25))
        self.rem3.setMaximumSize(QSize(25, 25))

        self.gridLayout_2.addWidget(self.rem3, 5, 2, 1, 1)

        self.label_5 = QLabel(self.argumentsPane)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setMinimumSize(QSize(70, 25))
        self.label_5.setMaximumSize(QSize(75, 25))
        self.label_5.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_2.addWidget(self.label_5, 6, 0, 1, 1)

        self.addfloat = QPushButton(self.argumentsPane)
        self.addfloat.setObjectName(u"addfloat")
        sizePolicy.setHeightForWidth(self.addfloat.sizePolicy().hasHeightForWidth())
        self.addfloat.setSizePolicy(sizePolicy)
        self.addfloat.setMinimumSize(QSize(25, 25))
        self.addfloat.setMaximumSize(QSize(25, 25))

        self.gridLayout_2.addWidget(self.addfloat, 6, 1, 1, 1)

        self.rem4 = QPushButton(self.argumentsPane)
        self.rem4.setObjectName(u"rem4")
        sizePolicy.setHeightForWidth(self.rem4.sizePolicy().hasHeightForWidth())
        self.rem4.setSizePolicy(sizePolicy)
        self.rem4.setMinimumSize(QSize(25, 25))
        self.rem4.setMaximumSize(QSize(25, 25))

        self.gridLayout_2.addWidget(self.rem4, 6, 2, 1, 1)

        self.label_6 = QLabel(self.argumentsPane)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setMinimumSize(QSize(70, 25))
        self.label_6.setMaximumSize(QSize(75, 25))
        self.label_6.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_2.addWidget(self.label_6, 7, 0, 1, 1)

        self.addchar = QPushButton(self.argumentsPane)
        self.addchar.setObjectName(u"addchar")
        sizePolicy.setHeightForWidth(self.addchar.sizePolicy().hasHeightForWidth())
        self.addchar.setSizePolicy(sizePolicy)
        self.addchar.setMinimumSize(QSize(25, 25))
        self.addchar.setMaximumSize(QSize(25, 25))

        self.gridLayout_2.addWidget(self.addchar, 7, 1, 1, 1)

        self.rem5 = QPushButton(self.argumentsPane)
        self.rem5.setObjectName(u"rem5")
        sizePolicy.setHeightForWidth(self.rem5.sizePolicy().hasHeightForWidth())
        self.rem5.setSizePolicy(sizePolicy)
        self.rem5.setMinimumSize(QSize(25, 25))
        self.rem5.setMaximumSize(QSize(25, 25))

        self.gridLayout_2.addWidget(self.rem5, 7, 2, 1, 1)

        self.label_7 = QLabel(self.argumentsPane)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setMinimumSize(QSize(70, 25))
        self.label_7.setMaximumSize(QSize(75, 25))
        self.label_7.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_2.addWidget(self.label_7, 8, 0, 1, 1)

        self.addstartstop = QPushButton(self.argumentsPane)
        self.addstartstop.setObjectName(u"addstartstop")
        sizePolicy.setHeightForWidth(self.addstartstop.sizePolicy().hasHeightForWidth())
        self.addstartstop.setSizePolicy(sizePolicy)
        self.addstartstop.setMinimumSize(QSize(25, 25))
        self.addstartstop.setMaximumSize(QSize(25, 25))

        self.gridLayout_2.addWidget(self.addstartstop, 8, 1, 1, 1)

        self.rem6 = QPushButton(self.argumentsPane)
        self.rem6.setObjectName(u"rem6")
        sizePolicy.setHeightForWidth(self.rem6.sizePolicy().hasHeightForWidth())
        self.rem6.setSizePolicy(sizePolicy)
        self.rem6.setMinimumSize(QSize(25, 25))
        self.rem6.setMaximumSize(QSize(25, 25))

        self.gridLayout_2.addWidget(self.rem6, 8, 2, 1, 1)

        self.label_8 = QLabel(self.argumentsPane)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setMinimumSize(QSize(70, 25))
        self.label_8.setMaximumSize(QSize(75, 25))
        self.label_8.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_2.addWidget(self.label_8, 9, 0, 1, 1)

        self.addnotype = QPushButton(self.argumentsPane)
        self.addnotype.setObjectName(u"addnotype")
        sizePolicy.setHeightForWidth(self.addnotype.sizePolicy().hasHeightForWidth())
        self.addnotype.setSizePolicy(sizePolicy)
        self.addnotype.setMinimumSize(QSize(25, 25))
        self.addnotype.setMaximumSize(QSize(25, 25))

        self.gridLayout_2.addWidget(self.addnotype, 9, 1, 1, 1)

        self.rem7 = QPushButton(self.argumentsPane)
        self.rem7.setObjectName(u"rem7")
        sizePolicy.setHeightForWidth(self.rem7.sizePolicy().hasHeightForWidth())
        self.rem7.setSizePolicy(sizePolicy)
        self.rem7.setMinimumSize(QSize(25, 25))
        self.rem7.setMaximumSize(QSize(25, 25))

        self.gridLayout_2.addWidget(self.rem7, 9, 2, 1, 1)

        self.label_10 = QLabel(self.argumentsPane)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setMinimumSize(QSize(125, 25))
        self.label_10.setMaximumSize(QSize(250, 25))
        self.label_10.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_2.addWidget(self.label_10, 10, 0, 1, 3)

        self.functionName = QLineEdit(self.argumentsPane)
        self.functionName.setObjectName(u"functionName")
        self.functionName.setMinimumSize(QSize(0, 25))
        self.functionName.setMaximumSize(QSize(250, 16777215))

        self.gridLayout_2.addWidget(self.functionName, 10, 3, 1, 1)


        self.gridLayout.addWidget(self.argumentsPane, 0, 1, 1, 1)


        self.retranslateUi(commandParametersDialog)

        QMetaObject.connectSlotsByName(commandParametersDialog)
    # setupUi

    def retranslateUi(self, commandParametersDialog):
        commandParametersDialog.setWindowTitle(QCoreApplication.translate("commandParametersDialog", u"Command Parameters", None))
        self.label_11.setText(QCoreApplication.translate("commandParametersDialog", u"Command string", None))
        self.label_13.setText(QCoreApplication.translate("commandParametersDialog", u"Command length", None))
        self.commandLengthLabel.setText(QCoreApplication.translate("commandParametersDialog", u"0", None))
        self.label_15.setText(QCoreApplication.translate("commandParametersDialog", u"Parent id", None))
        self.label_14.setText(QCoreApplication.translate("commandParametersDialog", u"id", None))
        self.commandHasWildcards.setText(QCoreApplication.translate("commandParametersDialog", u"Contains Wildcards", None))
        self.label_12.setText(QCoreApplication.translate("commandParametersDialog", u"Command depth", None))
        self.commandSubcommands_label.setText(QCoreApplication.translate("commandParametersDialog", u"Subcommands", None))
        self.label_16.setText(QCoreApplication.translate("commandParametersDialog", u"Arg. Handling", None))
        self.commandArgumentHandling.setItemText(0, QCoreApplication.translate("commandParametersDialog", u"No arguments", None))
        self.commandArgumentHandling.setItemText(1, QCoreApplication.translate("commandParametersDialog", u"Single argument type", None))
        self.commandArgumentHandling.setItemText(2, QCoreApplication.translate("commandParametersDialog", u"Argument type array", None))

        self.commandArgumentHandling.setCurrentText(QCoreApplication.translate("commandParametersDialog", u"No arguments", None))
        self.label_9.setText(QCoreApplication.translate("commandParametersDialog", u"Min. args.", None))
        self.argumentsPlainTextCSV.setPlaceholderText(QCoreApplication.translate("commandParametersDialog", u"Arguments...", None))
        self.commandMaxArgsLabel.setText(QCoreApplication.translate("commandParametersDialog", u"Max args.", None))
        self.label.setText(QCoreApplication.translate("commandParametersDialog", u"UINT8_T", None))
        self.add8bituint.setText(QCoreApplication.translate("commandParametersDialog", u"+", None))
        self.rem.setText(QCoreApplication.translate("commandParametersDialog", u"-", None))
        self.label_3.setText(QCoreApplication.translate("commandParametersDialog", u"UINT16_T", None))
        self.add16bituint.setText(QCoreApplication.translate("commandParametersDialog", u"+", None))
        self.rem1.setText(QCoreApplication.translate("commandParametersDialog", u"-", None))
        self.label_2.setText(QCoreApplication.translate("commandParametersDialog", u"UINT32_T", None))
        self.add32bituint.setText(QCoreApplication.translate("commandParametersDialog", u"+", None))
        self.rem2.setText(QCoreApplication.translate("commandParametersDialog", u"-", None))
        self.label_4.setText(QCoreApplication.translate("commandParametersDialog", u"INT16_T", None))
        self.add16bitint.setText(QCoreApplication.translate("commandParametersDialog", u"+", None))
        self.rem3.setText(QCoreApplication.translate("commandParametersDialog", u"-", None))
        self.label_5.setText(QCoreApplication.translate("commandParametersDialog", u"FLOAT", None))
        self.addfloat.setText(QCoreApplication.translate("commandParametersDialog", u"+", None))
        self.rem4.setText(QCoreApplication.translate("commandParametersDialog", u"-", None))
        self.label_6.setText(QCoreApplication.translate("commandParametersDialog", u"CHAR", None))
        self.addchar.setText(QCoreApplication.translate("commandParametersDialog", u"+", None))
        self.rem5.setText(QCoreApplication.translate("commandParametersDialog", u"-", None))
        self.label_7.setText(QCoreApplication.translate("commandParametersDialog", u"START_STOP", None))
        self.addstartstop.setText(QCoreApplication.translate("commandParametersDialog", u"+", None))
        self.rem6.setText(QCoreApplication.translate("commandParametersDialog", u"-", None))
        self.label_8.setText(QCoreApplication.translate("commandParametersDialog", u"NOTYPE", None))
        self.addnotype.setText(QCoreApplication.translate("commandParametersDialog", u"+", None))
        self.rem7.setText(QCoreApplication.translate("commandParametersDialog", u"-", None))
        self.label_10.setText(QCoreApplication.translate("commandParametersDialog", u"Return function name", None))
    # retranslateUi

