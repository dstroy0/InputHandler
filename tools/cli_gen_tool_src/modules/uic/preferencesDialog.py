# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'preferencesDialog.ui'
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
    QFormLayout, QFrame, QGridLayout, QLabel,
    QLineEdit, QPushButton, QSizePolicy, QVBoxLayout,
    QWidget)

class Ui_Preferences(object):
    def setupUi(self, Preferences):
        if not Preferences.objectName():
            Preferences.setObjectName(u"Preferences")
        Preferences.resize(537, 242)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Preferences.sizePolicy().hasHeightForWidth())
        Preferences.setSizePolicy(sizePolicy)
        Preferences.setMinimumSize(QSize(0, 0))
        self.gridLayout_3 = QGridLayout(Preferences)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.frame_4 = QFrame(Preferences)
        self.frame_4.setObjectName(u"frame_4")
        sizePolicy.setHeightForWidth(self.frame_4.sizePolicy().hasHeightForWidth())
        self.frame_4.setSizePolicy(sizePolicy)
        self.frame_4.setFrameShape(QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QFrame.Raised)
        self.gridLayout = QGridLayout(self.frame_4)
        self.gridLayout.setObjectName(u"gridLayout")
        self.label = QLabel(self.frame_4)
        self.label.setObjectName(u"label")
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setMinimumSize(QSize(120, 0))
        self.label.setMaximumSize(QSize(120, 25))
        self.label.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)

        self.output_path_input = QLineEdit(self.frame_4)
        self.output_path_input.setObjectName(u"output_path_input")
        sizePolicy1 = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.output_path_input.sizePolicy().hasHeightForWidth())
        self.output_path_input.setSizePolicy(sizePolicy1)
        self.output_path_input.setMinimumSize(QSize(0, 0))
        self.output_path_input.setReadOnly(True)

        self.gridLayout.addWidget(self.output_path_input, 2, 1, 1, 1)

        self.label_6 = QLabel(self.frame_4)
        self.label_6.setObjectName(u"label_6")
        sizePolicy.setHeightForWidth(self.label_6.sizePolicy().hasHeightForWidth())
        self.label_6.setSizePolicy(sizePolicy)
        self.label_6.setMinimumSize(QSize(120, 0))
        self.label_6.setMaximumSize(QSize(120, 25))
        self.label_6.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.label_6, 2, 0, 1, 1)

        self.config_path_input = QLineEdit(self.frame_4)
        self.config_path_input.setObjectName(u"config_path_input")
        sizePolicy1.setHeightForWidth(self.config_path_input.sizePolicy().hasHeightForWidth())
        self.config_path_input.setSizePolicy(sizePolicy1)
        self.config_path_input.setReadOnly(True)

        self.gridLayout.addWidget(self.config_path_input, 1, 1, 1, 1)

        self.browse_for_config = QPushButton(self.frame_4)
        self.browse_for_config.setObjectName(u"browse_for_config")

        self.gridLayout.addWidget(self.browse_for_config, 1, 2, 1, 1)

        self.browse_for_output_dir = QPushButton(self.frame_4)
        self.browse_for_output_dir.setObjectName(u"browse_for_output_dir")

        self.gridLayout.addWidget(self.browse_for_output_dir, 2, 2, 1, 1)

        self.label_12 = QLabel(self.frame_4)
        self.label_12.setObjectName(u"label_12")
        sizePolicy2 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.label_12.sizePolicy().hasHeightForWidth())
        self.label_12.setSizePolicy(sizePolicy2)
        self.label_12.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.label_12, 0, 0, 1, 3)


        self.gridLayout_3.addWidget(self.frame_4, 0, 0, 1, 3)

        self.cancel = QPushButton(Preferences)
        self.cancel.setObjectName(u"cancel")

        self.gridLayout_3.addWidget(self.cancel, 2, 2, 1, 1)

        self.frame_6 = QFrame(Preferences)
        self.frame_6.setObjectName(u"frame_6")
        sizePolicy2.setHeightForWidth(self.frame_6.sizePolicy().hasHeightForWidth())
        self.frame_6.setSizePolicy(sizePolicy2)
        self.frame_6.setMinimumSize(QSize(120, 20))
        self.frame_6.setFrameShape(QFrame.NoFrame)
        self.frame_6.setFrameShadow(QFrame.Plain)

        self.gridLayout_3.addWidget(self.frame_6, 2, 3, 1, 1)

        self.ok = QPushButton(Preferences)
        self.ok.setObjectName(u"ok")

        self.gridLayout_3.addWidget(self.ok, 2, 1, 1, 1)

        self.frame_2 = QFrame(Preferences)
        self.frame_2.setObjectName(u"frame_2")
        sizePolicy.setHeightForWidth(self.frame_2.sizePolicy().hasHeightForWidth())
        self.frame_2.setSizePolicy(sizePolicy)
        self.frame_2.setFrameShape(QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.formLayout = QFormLayout(self.frame_2)
        self.formLayout.setObjectName(u"formLayout")
        self.label_7 = QLabel(self.frame_2)
        self.label_7.setObjectName(u"label_7")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label_7)

        self.default_stream = QLineEdit(self.frame_2)
        self.default_stream.setObjectName(u"default_stream")

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.default_stream)

        self.label_8 = QLabel(self.frame_2)
        self.label_8.setObjectName(u"label_8")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.label_8)

        self.default_output_buffer_size = QLineEdit(self.frame_2)
        self.default_output_buffer_size.setObjectName(u"default_output_buffer_size")

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.default_output_buffer_size)

        self.label_10 = QLabel(self.frame_2)
        self.label_10.setObjectName(u"label_10")
        sizePolicy2.setHeightForWidth(self.label_10.sizePolicy().hasHeightForWidth())
        self.label_10.setSizePolicy(sizePolicy2)
        self.label_10.setAlignment(Qt.AlignCenter)

        self.formLayout.setWidget(0, QFormLayout.SpanningRole, self.label_10)


        self.gridLayout_3.addWidget(self.frame_2, 1, 0, 1, 2)

        self.frame = QFrame(Preferences)
        self.frame.setObjectName(u"frame")
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setAutoFillBackground(False)
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.gridLayout_2 = QGridLayout(self.frame)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.listcommands_checkbox = QCheckBox(self.frame)
        self.listcommands_checkbox.setObjectName(u"listcommands_checkbox")

        self.gridLayout_2.addWidget(self.listcommands_checkbox, 1, 1, 1, 1)

        self.outputtostream_checkbox = QCheckBox(self.frame)
        self.outputtostream_checkbox.setObjectName(u"outputtostream_checkbox")

        self.gridLayout_2.addWidget(self.outputtostream_checkbox, 1, 0, 1, 1)

        self.defaultfunction_checkbox = QCheckBox(self.frame)
        self.defaultfunction_checkbox.setObjectName(u"defaultfunction_checkbox")

        self.gridLayout_2.addWidget(self.defaultfunction_checkbox, 2, 0, 1, 1)

        self.listsettings_checkbox = QCheckBox(self.frame)
        self.listsettings_checkbox.setObjectName(u"listsettings_checkbox")

        self.gridLayout_2.addWidget(self.listsettings_checkbox, 2, 1, 1, 1)

        self.label_9 = QLabel(self.frame)
        self.label_9.setObjectName(u"label_9")
        sizePolicy2.setHeightForWidth(self.label_9.sizePolicy().hasHeightForWidth())
        self.label_9.setSizePolicy(sizePolicy2)
        self.label_9.setAutoFillBackground(False)
        self.label_9.setAlignment(Qt.AlignCenter)

        self.gridLayout_2.addWidget(self.label_9, 0, 0, 1, 2)


        self.gridLayout_3.addWidget(self.frame, 1, 2, 1, 2)

        self.frame_5 = QFrame(Preferences)
        self.frame_5.setObjectName(u"frame_5")
        sizePolicy2.setHeightForWidth(self.frame_5.sizePolicy().hasHeightForWidth())
        self.frame_5.setSizePolicy(sizePolicy2)
        self.frame_5.setMinimumSize(QSize(120, 20))
        self.frame_5.setFrameShape(QFrame.NoFrame)
        self.frame_5.setFrameShadow(QFrame.Plain)

        self.gridLayout_3.addWidget(self.frame_5, 2, 0, 1, 1)

        self.frame_3 = QFrame(Preferences)
        self.frame_3.setObjectName(u"frame_3")
        sizePolicy.setHeightForWidth(self.frame_3.sizePolicy().hasHeightForWidth())
        self.frame_3.setSizePolicy(sizePolicy)
        self.frame_3.setMinimumSize(QSize(150, 0))
        self.frame_3.setFrameShape(QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Raised)
        self.verticalLayout = QVBoxLayout(self.frame_3)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label_11 = QLabel(self.frame_3)
        self.label_11.setObjectName(u"label_11")
        sizePolicy2.setHeightForWidth(self.label_11.sizePolicy().hasHeightForWidth())
        self.label_11.setSizePolicy(sizePolicy2)
        self.label_11.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.label_11)

        self.logLevelComboBox = QComboBox(self.frame_3)
        self.logLevelComboBox.addItem("")
        self.logLevelComboBox.addItem("")
        self.logLevelComboBox.addItem("")
        self.logLevelComboBox.addItem("")
        self.logLevelComboBox.addItem("")
        self.logLevelComboBox.setObjectName(u"logLevelComboBox")

        self.verticalLayout.addWidget(self.logLevelComboBox)


        self.gridLayout_3.addWidget(self.frame_3, 0, 3, 1, 1)


        self.retranslateUi(Preferences)

        self.logLevelComboBox.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(Preferences)
    # setupUi

    def retranslateUi(self, Preferences):
        Preferences.setWindowTitle(QCoreApplication.translate("Preferences", u"Preferences", None))
        self.label.setText(QCoreApplication.translate("Preferences", u"Input Config File Path", None))
        self.output_path_input.setPlaceholderText(QCoreApplication.translate("Preferences", u"Not set...", None))
        self.label_6.setText(QCoreApplication.translate("Preferences", u"Output Directory", None))
        self.config_path_input.setPlaceholderText(QCoreApplication.translate("Preferences", u"Not set...", None))
        self.browse_for_config.setText(QCoreApplication.translate("Preferences", u"Browse...", None))
        self.browse_for_output_dir.setText(QCoreApplication.translate("Preferences", u"Browse...", None))
        self.label_12.setText(QCoreApplication.translate("Preferences", u"Pathing", None))
        self.cancel.setText(QCoreApplication.translate("Preferences", u"Cancel", None))
        self.ok.setText(QCoreApplication.translate("Preferences", u"Ok", None))
        self.label_7.setText(QCoreApplication.translate("Preferences", u"Stream", None))
        self.default_stream.setText(QCoreApplication.translate("Preferences", u"Serial", None))
        self.default_stream.setPlaceholderText(QCoreApplication.translate("Preferences", u"output stream", None))
        self.label_8.setText(QCoreApplication.translate("Preferences", u"Buffer size", None))
        self.default_output_buffer_size.setText(QCoreApplication.translate("Preferences", u"700", None))
        self.default_output_buffer_size.setPlaceholderText(QCoreApplication.translate("Preferences", u"buffer size in bytes", None))
        self.label_10.setText(QCoreApplication.translate("Preferences", u"Output", None))
        self.listcommands_checkbox.setText(QCoreApplication.translate("Preferences", u"listCommands", None))
        self.outputtostream_checkbox.setText(QCoreApplication.translate("Preferences", u"outputToStream", None))
        self.defaultfunction_checkbox.setText(QCoreApplication.translate("Preferences", u"defaultFunction", None))
        self.listsettings_checkbox.setText(QCoreApplication.translate("Preferences", u"listSettings", None))
        self.label_9.setText(QCoreApplication.translate("Preferences", u"Builtin Methods", None))
        self.label_11.setText(QCoreApplication.translate("Preferences", u"Log Level", None))
        self.logLevelComboBox.setItemText(0, QCoreApplication.translate("Preferences", u"DEBUG", u"10"))
        self.logLevelComboBox.setItemText(1, QCoreApplication.translate("Preferences", u"INFO", u"20"))
        self.logLevelComboBox.setItemText(2, QCoreApplication.translate("Preferences", u"WARNING", u"30"))
        self.logLevelComboBox.setItemText(3, QCoreApplication.translate("Preferences", u"ERROR", u"40"))
        self.logLevelComboBox.setItemText(4, QCoreApplication.translate("Preferences", u"CRITICAL", u"50"))

        self.logLevelComboBox.setCurrentText(QCoreApplication.translate("Preferences", u"DEBUG", None))
    # retranslateUi

