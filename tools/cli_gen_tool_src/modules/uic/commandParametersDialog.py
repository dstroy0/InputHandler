# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'commandParametersDialog.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QDialog,
    QFrame, QGridLayout, QHeaderView, QLabel,
    QLineEdit, QPushButton, QSizePolicy, QSpinBox,
    QTableWidget, QTableWidgetItem, QWidget)

class Ui_commandParametersDialog(object):
    def setupUi(self, commandParametersDialog):
        if not commandParametersDialog.objectName():
            commandParametersDialog.setObjectName(u"commandParametersDialog")
        commandParametersDialog.resize(699, 358)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(commandParametersDialog.sizePolicy().hasHeightForWidth())
        commandParametersDialog.setSizePolicy(sizePolicy)
        self.gridLayout_3 = QGridLayout(commandParametersDialog)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.parametersPane = QWidget(commandParametersDialog)
        self.parametersPane.setObjectName(u"parametersPane")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.parametersPane.sizePolicy().hasHeightForWidth())
        self.parametersPane.setSizePolicy(sizePolicy1)
        self.parametersPane.setMinimumSize(QSize(300, 0))
        self.parametersPane.setMaximumSize(QSize(16777215, 16777215))
        self.gridLayout_2 = QGridLayout(self.parametersPane)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.label_11 = QLabel(self.parametersPane)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setMinimumSize(QSize(125, 24))
        self.label_11.setMaximumSize(QSize(125, 24))
        self.label_11.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_2.addWidget(self.label_11, 0, 0, 1, 1)

        self.commandString = QLineEdit(self.parametersPane)
        self.commandString.setObjectName(u"commandString")
        sizePolicy2 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.commandString.sizePolicy().hasHeightForWidth())
        self.commandString.setSizePolicy(sizePolicy2)
        self.commandString.setMinimumSize(QSize(150, 24))
        self.commandString.setMaximumSize(QSize(16777215, 24))

        self.gridLayout_2.addWidget(self.commandString, 0, 1, 1, 1)

        self.label_13 = QLabel(self.parametersPane)
        self.label_13.setObjectName(u"label_13")
        sizePolicy.setHeightForWidth(self.label_13.sizePolicy().hasHeightForWidth())
        self.label_13.setSizePolicy(sizePolicy)
        self.label_13.setMinimumSize(QSize(125, 24))
        self.label_13.setMaximumSize(QSize(125, 24))
        self.label_13.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_2.addWidget(self.label_13, 1, 0, 1, 1)

        self.commandLengthLabel = QLabel(self.parametersPane)
        self.commandLengthLabel.setObjectName(u"commandLengthLabel")
        sizePolicy.setHeightForWidth(self.commandLengthLabel.sizePolicy().hasHeightForWidth())
        self.commandLengthLabel.setSizePolicy(sizePolicy)
        self.commandLengthLabel.setMinimumSize(QSize(150, 24))
        self.commandLengthLabel.setMaximumSize(QSize(16777215, 24))

        self.gridLayout_2.addWidget(self.commandLengthLabel, 1, 1, 1, 1)

        self.label_15 = QLabel(self.parametersPane)
        self.label_15.setObjectName(u"label_15")
        sizePolicy.setHeightForWidth(self.label_15.sizePolicy().hasHeightForWidth())
        self.label_15.setSizePolicy(sizePolicy)
        self.label_15.setMinimumSize(QSize(125, 20))
        self.label_15.setMaximumSize(QSize(125, 20))
        self.label_15.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_2.addWidget(self.label_15, 2, 0, 1, 1)

        self.commandParentId = QLineEdit(self.parametersPane)
        self.commandParentId.setObjectName(u"commandParentId")
        sizePolicy2.setHeightForWidth(self.commandParentId.sizePolicy().hasHeightForWidth())
        self.commandParentId.setSizePolicy(sizePolicy2)
        self.commandParentId.setMinimumSize(QSize(150, 24))
        self.commandParentId.setMaximumSize(QSize(16777215, 24))

        self.gridLayout_2.addWidget(self.commandParentId, 2, 1, 1, 1)

        self.label_14 = QLabel(self.parametersPane)
        self.label_14.setObjectName(u"label_14")
        sizePolicy.setHeightForWidth(self.label_14.sizePolicy().hasHeightForWidth())
        self.label_14.setSizePolicy(sizePolicy)
        self.label_14.setMinimumSize(QSize(125, 24))
        self.label_14.setMaximumSize(QSize(125, 24))
        self.label_14.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_2.addWidget(self.label_14, 3, 0, 1, 1)

        self.commandId = QLineEdit(self.parametersPane)
        self.commandId.setObjectName(u"commandId")
        sizePolicy2.setHeightForWidth(self.commandId.sizePolicy().hasHeightForWidth())
        self.commandId.setSizePolicy(sizePolicy2)
        self.commandId.setMinimumSize(QSize(150, 24))
        self.commandId.setMaximumSize(QSize(16777215, 24))

        self.gridLayout_2.addWidget(self.commandId, 3, 1, 1, 1)

        self.frame_6 = QFrame(self.parametersPane)
        self.frame_6.setObjectName(u"frame_6")
        sizePolicy.setHeightForWidth(self.frame_6.sizePolicy().hasHeightForWidth())
        self.frame_6.setSizePolicy(sizePolicy)
        self.frame_6.setMinimumSize(QSize(125, 24))
        self.frame_6.setMaximumSize(QSize(125, 24))
        self.frame_6.setFrameShape(QFrame.NoFrame)
        self.frame_6.setFrameShadow(QFrame.Plain)

        self.gridLayout_2.addWidget(self.frame_6, 4, 0, 1, 1)

        self.commandHasWildcards = QCheckBox(self.parametersPane)
        self.commandHasWildcards.setObjectName(u"commandHasWildcards")
        sizePolicy2.setHeightForWidth(self.commandHasWildcards.sizePolicy().hasHeightForWidth())
        self.commandHasWildcards.setSizePolicy(sizePolicy2)
        self.commandHasWildcards.setMinimumSize(QSize(150, 24))
        self.commandHasWildcards.setMaximumSize(QSize(16777215, 24))

        self.gridLayout_2.addWidget(self.commandHasWildcards, 4, 1, 1, 1)

        self.label_12 = QLabel(self.parametersPane)
        self.label_12.setObjectName(u"label_12")
        sizePolicy.setHeightForWidth(self.label_12.sizePolicy().hasHeightForWidth())
        self.label_12.setSizePolicy(sizePolicy)
        self.label_12.setMinimumSize(QSize(125, 24))
        self.label_12.setMaximumSize(QSize(125, 24))
        self.label_12.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_2.addWidget(self.label_12, 5, 0, 1, 1)

        self.commandDepth = QSpinBox(self.parametersPane)
        self.commandDepth.setObjectName(u"commandDepth")
        sizePolicy2.setHeightForWidth(self.commandDepth.sizePolicy().hasHeightForWidth())
        self.commandDepth.setSizePolicy(sizePolicy2)
        self.commandDepth.setMinimumSize(QSize(150, 24))
        self.commandDepth.setMaximumSize(QSize(16777215, 24))

        self.gridLayout_2.addWidget(self.commandDepth, 5, 1, 1, 1)

        self.commandSubcommands_label = QLabel(self.parametersPane)
        self.commandSubcommands_label.setObjectName(u"commandSubcommands_label")
        sizePolicy.setHeightForWidth(self.commandSubcommands_label.sizePolicy().hasHeightForWidth())
        self.commandSubcommands_label.setSizePolicy(sizePolicy)
        self.commandSubcommands_label.setMinimumSize(QSize(125, 24))
        self.commandSubcommands_label.setMaximumSize(QSize(125, 24))
        self.commandSubcommands_label.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_2.addWidget(self.commandSubcommands_label, 6, 0, 1, 1)

        self.commandSubcommands = QSpinBox(self.parametersPane)
        self.commandSubcommands.setObjectName(u"commandSubcommands")
        sizePolicy2.setHeightForWidth(self.commandSubcommands.sizePolicy().hasHeightForWidth())
        self.commandSubcommands.setSizePolicy(sizePolicy2)
        self.commandSubcommands.setMinimumSize(QSize(150, 24))
        self.commandSubcommands.setMaximumSize(QSize(16777215, 24))

        self.gridLayout_2.addWidget(self.commandSubcommands, 6, 1, 1, 1)

        self.label_16 = QLabel(self.parametersPane)
        self.label_16.setObjectName(u"label_16")
        sizePolicy.setHeightForWidth(self.label_16.sizePolicy().hasHeightForWidth())
        self.label_16.setSizePolicy(sizePolicy)
        self.label_16.setMinimumSize(QSize(125, 24))
        self.label_16.setMaximumSize(QSize(125, 24))
        self.label_16.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_2.addWidget(self.label_16, 7, 0, 1, 1)

        self.commandArgumentHandling = QComboBox(self.parametersPane)
        self.commandArgumentHandling.addItem("")
        self.commandArgumentHandling.addItem("")
        self.commandArgumentHandling.addItem("")
        self.commandArgumentHandling.setObjectName(u"commandArgumentHandling")
        sizePolicy2.setHeightForWidth(self.commandArgumentHandling.sizePolicy().hasHeightForWidth())
        self.commandArgumentHandling.setSizePolicy(sizePolicy2)
        self.commandArgumentHandling.setMinimumSize(QSize(150, 24))
        self.commandArgumentHandling.setMaximumSize(QSize(16777215, 24))

        self.gridLayout_2.addWidget(self.commandArgumentHandling, 7, 1, 1, 1)

        self.label_10 = QLabel(self.parametersPane)
        self.label_10.setObjectName(u"label_10")
        sizePolicy.setHeightForWidth(self.label_10.sizePolicy().hasHeightForWidth())
        self.label_10.setSizePolicy(sizePolicy)
        self.label_10.setMinimumSize(QSize(125, 24))
        self.label_10.setMaximumSize(QSize(125, 24))
        self.label_10.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_2.addWidget(self.label_10, 8, 0, 1, 1)

        self.returnFunctionName = QLineEdit(self.parametersPane)
        self.returnFunctionName.setObjectName(u"returnFunctionName")
        sizePolicy2.setHeightForWidth(self.returnFunctionName.sizePolicy().hasHeightForWidth())
        self.returnFunctionName.setSizePolicy(sizePolicy2)
        self.returnFunctionName.setMinimumSize(QSize(150, 24))
        self.returnFunctionName.setMaximumSize(QSize(16777215, 24))

        self.gridLayout_2.addWidget(self.returnFunctionName, 8, 1, 1, 1)


        self.gridLayout_3.addWidget(self.parametersPane, 0, 0, 1, 2)

        self.argumentsPane = QWidget(commandParametersDialog)
        self.argumentsPane.setObjectName(u"argumentsPane")
        sizePolicy1.setHeightForWidth(self.argumentsPane.sizePolicy().hasHeightForWidth())
        self.argumentsPane.setSizePolicy(sizePolicy1)
        self.argumentsPane.setMinimumSize(QSize(375, 310))
        self.gridLayout = QGridLayout(self.argumentsPane)
        self.gridLayout.setObjectName(u"gridLayout")
        self.argTable = QTableWidget(self.argumentsPane)
        self.argTable.setObjectName(u"argTable")

        self.gridLayout.addWidget(self.argTable, 1, 0, 1, 5)

        self.argComboBox = QComboBox(self.argumentsPane)
        self.argComboBox.setObjectName(u"argComboBox")
        sizePolicy.setHeightForWidth(self.argComboBox.sizePolicy().hasHeightForWidth())
        self.argComboBox.setSizePolicy(sizePolicy)
        self.argComboBox.setMinimumSize(QSize(100, 24))
        self.argComboBox.setMaximumSize(QSize(100, 24))

        self.gridLayout.addWidget(self.argComboBox, 2, 1, 1, 2)

        self.insert = QPushButton(self.argumentsPane)
        self.insert.setObjectName(u"insert")
        sizePolicy.setHeightForWidth(self.insert.sizePolicy().hasHeightForWidth())
        self.insert.setSizePolicy(sizePolicy)
        self.insert.setMinimumSize(QSize(75, 24))
        self.insert.setMaximumSize(QSize(75, 24))

        self.gridLayout.addWidget(self.insert, 2, 3, 1, 1)

        self.commandMinArgs = QSpinBox(self.argumentsPane)
        self.commandMinArgs.setObjectName(u"commandMinArgs")
        sizePolicy.setHeightForWidth(self.commandMinArgs.sizePolicy().hasHeightForWidth())
        self.commandMinArgs.setSizePolicy(sizePolicy)
        self.commandMinArgs.setMinimumSize(QSize(75, 24))
        self.commandMinArgs.setMaximumSize(QSize(75, 24))

        self.gridLayout.addWidget(self.commandMinArgs, 0, 1, 1, 1)

        self.commandMaxArgsLabel = QLabel(self.argumentsPane)
        self.commandMaxArgsLabel.setObjectName(u"commandMaxArgsLabel")
        sizePolicy.setHeightForWidth(self.commandMaxArgsLabel.sizePolicy().hasHeightForWidth())
        self.commandMaxArgsLabel.setSizePolicy(sizePolicy)
        self.commandMaxArgsLabel.setMinimumSize(QSize(70, 24))
        self.commandMaxArgsLabel.setMaximumSize(QSize(75, 24))
        self.commandMaxArgsLabel.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.commandMaxArgsLabel, 0, 2, 1, 2)

        self.frame_5 = QFrame(self.argumentsPane)
        self.frame_5.setObjectName(u"frame_5")
        sizePolicy2.setHeightForWidth(self.frame_5.sizePolicy().hasHeightForWidth())
        self.frame_5.setSizePolicy(sizePolicy2)
        self.frame_5.setMinimumSize(QSize(80, 24))
        self.frame_5.setMaximumSize(QSize(16777215, 24))
        self.frame_5.setFrameShape(QFrame.NoFrame)
        self.frame_5.setFrameShadow(QFrame.Plain)

        self.gridLayout.addWidget(self.frame_5, 2, 4, 1, 1)

        self.label_9 = QLabel(self.argumentsPane)
        self.label_9.setObjectName(u"label_9")
        sizePolicy.setHeightForWidth(self.label_9.sizePolicy().hasHeightForWidth())
        self.label_9.setSizePolicy(sizePolicy)
        self.label_9.setMinimumSize(QSize(70, 24))
        self.label_9.setMaximumSize(QSize(70, 24))
        self.label_9.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.label_9, 0, 0, 1, 1)

        self.frame_4 = QFrame(self.argumentsPane)
        self.frame_4.setObjectName(u"frame_4")
        sizePolicy2.setHeightForWidth(self.frame_4.sizePolicy().hasHeightForWidth())
        self.frame_4.setSizePolicy(sizePolicy2)
        self.frame_4.setMinimumSize(QSize(70, 24))
        self.frame_4.setMaximumSize(QSize(16777215, 24))
        self.frame_4.setFrameShape(QFrame.NoFrame)
        self.frame_4.setFrameShadow(QFrame.Plain)

        self.gridLayout.addWidget(self.frame_4, 2, 0, 1, 1)

        self.commandMaxArgs = QSpinBox(self.argumentsPane)
        self.commandMaxArgs.setObjectName(u"commandMaxArgs")
        sizePolicy1.setHeightForWidth(self.commandMaxArgs.sizePolicy().hasHeightForWidth())
        self.commandMaxArgs.setSizePolicy(sizePolicy1)
        self.commandMaxArgs.setMinimumSize(QSize(70, 24))
        self.commandMaxArgs.setMaximumSize(QSize(70, 24))

        self.gridLayout.addWidget(self.commandMaxArgs, 0, 4, 1, 1)


        self.gridLayout_3.addWidget(self.argumentsPane, 0, 2, 1, 3)

        self.frame_2 = QFrame(commandParametersDialog)
        self.frame_2.setObjectName(u"frame_2")
        sizePolicy2.setHeightForWidth(self.frame_2.sizePolicy().hasHeightForWidth())
        self.frame_2.setSizePolicy(sizePolicy2)
        self.frame_2.setMinimumSize(QSize(0, 20))
        self.frame_2.setMaximumSize(QSize(16777215, 20))
        self.frame_2.setFrameShape(QFrame.NoFrame)
        self.frame_2.setFrameShadow(QFrame.Plain)

        self.gridLayout_3.addWidget(self.frame_2, 1, 0, 1, 1)

        self.reset = QPushButton(commandParametersDialog)
        self.reset.setObjectName(u"reset")
        sizePolicy.setHeightForWidth(self.reset.sizePolicy().hasHeightForWidth())
        self.reset.setSizePolicy(sizePolicy)

        self.gridLayout_3.addWidget(self.reset, 1, 1, 1, 1)

        self.ok = QPushButton(commandParametersDialog)
        self.ok.setObjectName(u"ok")
        sizePolicy.setHeightForWidth(self.ok.sizePolicy().hasHeightForWidth())
        self.ok.setSizePolicy(sizePolicy)

        self.gridLayout_3.addWidget(self.ok, 1, 2, 1, 1)

        self.cancel = QPushButton(commandParametersDialog)
        self.cancel.setObjectName(u"cancel")
        sizePolicy.setHeightForWidth(self.cancel.sizePolicy().hasHeightForWidth())
        self.cancel.setSizePolicy(sizePolicy)

        self.gridLayout_3.addWidget(self.cancel, 1, 3, 1, 1)

        self.frame_3 = QFrame(commandParametersDialog)
        self.frame_3.setObjectName(u"frame_3")
        sizePolicy2.setHeightForWidth(self.frame_3.sizePolicy().hasHeightForWidth())
        self.frame_3.setSizePolicy(sizePolicy2)
        self.frame_3.setMinimumSize(QSize(0, 20))
        self.frame_3.setMaximumSize(QSize(16777215, 20))
        self.frame_3.setFrameShape(QFrame.NoFrame)
        self.frame_3.setFrameShadow(QFrame.Plain)

        self.gridLayout_3.addWidget(self.frame_3, 1, 4, 1, 1)


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
        self.label_10.setText(QCoreApplication.translate("commandParametersDialog", u"Return function name", None))
        self.insert.setText(QCoreApplication.translate("commandParametersDialog", u"Insert", None))
        self.commandMaxArgsLabel.setText(QCoreApplication.translate("commandParametersDialog", u"Max args.", None))
        self.label_9.setText(QCoreApplication.translate("commandParametersDialog", u"Min. args.", None))
        self.reset.setText(QCoreApplication.translate("commandParametersDialog", u"Reset", None))
        self.ok.setText(QCoreApplication.translate("commandParametersDialog", u"Ok", None))
        self.cancel.setText(QCoreApplication.translate("commandParametersDialog", u"Cancel", None))
    # retranslateUi

