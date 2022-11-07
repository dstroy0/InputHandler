# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainWindow.ui'
##
## Created by: Qt User Interface Compiler version 6.3.2
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
from PySide6.QtWidgets import (QAbstractScrollArea, QApplication, QGridLayout, QHeaderView,
    QLabel, QMainWindow, QMenu, QMenuBar,
    QPushButton, QSizePolicy, QSplitter, QTabWidget,
    QTreeWidget, QTreeWidgetItem, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1460, 885)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QSize(0, 0))
        MainWindow.setMouseTracking(False)
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
        self.actionGenerate_CLI_Files = QAction(MainWindow)
        self.actionGenerate_CLI_Files.setObjectName(u"actionGenerate_CLI_Files")
        self.actionSave_As = QAction(MainWindow)
        self.actionSave_As.setObjectName(u"actionSave_As")
        self.actionExit = QAction(MainWindow)
        self.actionExit.setObjectName(u"actionExit")
        self.actionOpen_Log_History = QAction(MainWindow)
        self.actionOpen_Log_History.setObjectName(u"actionOpen_Log_History")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.centralwidget.setEnabled(True)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setMinimumSize(QSize(0, 0))
        self.centralwidget.setMouseTracking(False)
        self.centralwidget.setLayoutDirection(Qt.LeftToRight)
        self.gridLayout_4 = QGridLayout(self.centralwidget)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        sizePolicy.setHeightForWidth(self.tabWidget.sizePolicy().hasHeightForWidth())
        self.tabWidget.setSizePolicy(sizePolicy)
        self.tabWidget.setMinimumSize(QSize(0, 0))
        self.tabWidget.setSizeIncrement(QSize(0, 0))
        self.tabWidget.setMouseTracking(False)
        self.tabWidget.setAutoFillBackground(True)
        self.ih_settings_tab = QWidget()
        self.ih_settings_tab.setObjectName(u"ih_settings_tab")
        sizePolicy.setHeightForWidth(self.ih_settings_tab.sizePolicy().hasHeightForWidth())
        self.ih_settings_tab.setSizePolicy(sizePolicy)
        self.ih_settings_tab.setMouseTracking(False)
        self.gridLayout_3 = QGridLayout(self.ih_settings_tab)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.splitter_2 = QSplitter(self.ih_settings_tab)
        self.splitter_2.setObjectName(u"splitter_2")
        sizePolicy.setHeightForWidth(self.splitter_2.sizePolicy().hasHeightForWidth())
        self.splitter_2.setSizePolicy(sizePolicy)
        self.splitter_2.setOrientation(Qt.Horizontal)
        self.widget = QWidget(self.splitter_2)
        self.widget.setObjectName(u"widget")
        sizePolicy.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(sizePolicy)
        self.gridLayout_2 = QGridLayout(self.widget)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.clear_setting_button = QPushButton(self.widget)
        self.clear_setting_button.setObjectName(u"clear_setting_button")
        sizePolicy1 = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.clear_setting_button.sizePolicy().hasHeightForWidth())
        self.clear_setting_button.setSizePolicy(sizePolicy1)

        self.gridLayout_2.addWidget(self.clear_setting_button, 4, 1, 1, 1)

        self.edit_setting_button = QPushButton(self.widget)
        self.edit_setting_button.setObjectName(u"edit_setting_button")
        sizePolicy1.setHeightForWidth(self.edit_setting_button.sizePolicy().hasHeightForWidth())
        self.edit_setting_button.setSizePolicy(sizePolicy1)

        self.gridLayout_2.addWidget(self.edit_setting_button, 4, 0, 1, 1)

        self.default_setting_button = QPushButton(self.widget)
        self.default_setting_button.setObjectName(u"default_setting_button")
        sizePolicy1.setHeightForWidth(self.default_setting_button.sizePolicy().hasHeightForWidth())
        self.default_setting_button.setSizePolicy(sizePolicy1)

        self.gridLayout_2.addWidget(self.default_setting_button, 4, 2, 1, 1)

        self.settings_tree = QTreeWidget(self.widget)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setText(0, u"1");
        self.settings_tree.setHeaderItem(__qtreewidgetitem)
        self.settings_tree.setObjectName(u"settings_tree")
        sizePolicy.setHeightForWidth(self.settings_tree.sizePolicy().hasHeightForWidth())
        self.settings_tree.setSizePolicy(sizePolicy)
        self.settings_tree.setMinimumSize(QSize(0, 0))
        self.settings_tree.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.settings_tree.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.settings_tree.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.settings_tree.setDragEnabled(False)

        self.gridLayout_2.addWidget(self.settings_tree, 3, 0, 1, 3)

        self.settings_tree_collapse_button = QPushButton(self.widget)
        self.settings_tree_collapse_button.setObjectName(u"settings_tree_collapse_button")
        self.settings_tree_collapse_button.setMaximumSize(QSize(150, 16777215))

        self.gridLayout_2.addWidget(self.settings_tree_collapse_button, 1, 0, 1, 1)

        self.tab_1_settings_table_label = QLabel(self.widget)
        self.tab_1_settings_table_label.setObjectName(u"tab_1_settings_table_label")
        sizePolicy2 = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Minimum)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.tab_1_settings_table_label.sizePolicy().hasHeightForWidth())
        self.tab_1_settings_table_label.setSizePolicy(sizePolicy2)
        self.tab_1_settings_table_label.setMinimumSize(QSize(0, 0))
        self.tab_1_settings_table_label.setAlignment(Qt.AlignCenter)

        self.gridLayout_2.addWidget(self.tab_1_settings_table_label, 1, 1, 1, 1)

        self.splitter_2.addWidget(self.widget)
        self.code_preview_container = QWidget(self.splitter_2)
        self.code_preview_container.setObjectName(u"code_preview_container")
        sizePolicy.setHeightForWidth(self.code_preview_container.sizePolicy().hasHeightForWidth())
        self.code_preview_container.setSizePolicy(sizePolicy)
        self.gridLayout = QGridLayout(self.code_preview_container)
        self.gridLayout.setObjectName(u"gridLayout")
        self.tab_1_code_preview_label = QLabel(self.code_preview_container)
        self.tab_1_code_preview_label.setObjectName(u"tab_1_code_preview_label")
        sizePolicy2.setHeightForWidth(self.tab_1_code_preview_label.sizePolicy().hasHeightForWidth())
        self.tab_1_code_preview_label.setSizePolicy(sizePolicy2)
        self.tab_1_code_preview_label.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.tab_1_code_preview_label, 0, 0, 1, 1)

        self.codePreview_1 = QTreeWidget(self.code_preview_container)
        __qtreewidgetitem1 = QTreeWidgetItem()
        __qtreewidgetitem1.setText(0, u"1");
        self.codePreview_1.setHeaderItem(__qtreewidgetitem1)
        self.codePreview_1.setObjectName(u"codePreview_1")
        sizePolicy.setHeightForWidth(self.codePreview_1.sizePolicy().hasHeightForWidth())
        self.codePreview_1.setSizePolicy(sizePolicy)
        self.codePreview_1.setMinimumSize(QSize(0, 0))
        self.codePreview_1.setMouseTracking(False)
        self.codePreview_1.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.codePreview_1.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.codePreview_1.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.codePreview_1.setDragEnabled(False)

        self.gridLayout.addWidget(self.codePreview_1, 1, 0, 1, 1)

        self.splitter_2.addWidget(self.code_preview_container)

        self.gridLayout_3.addWidget(self.splitter_2, 0, 0, 1, 1)

        self.tabWidget.addTab(self.ih_settings_tab, "")
        self.command_tab = QWidget()
        self.command_tab.setObjectName(u"command_tab")
        sizePolicy.setHeightForWidth(self.command_tab.sizePolicy().hasHeightForWidth())
        self.command_tab.setSizePolicy(sizePolicy)
        self.command_tab.setMouseTracking(False)
        self.command_tab.setLayoutDirection(Qt.LeftToRight)
        self.gridLayout_5 = QGridLayout(self.command_tab)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.splitter = QSplitter(self.command_tab)
        self.splitter.setObjectName(u"splitter")
        sizePolicy.setHeightForWidth(self.splitter.sizePolicy().hasHeightForWidth())
        self.splitter.setSizePolicy(sizePolicy)
        self.splitter.setOrientation(Qt.Horizontal)
        self.commands_container = QWidget(self.splitter)
        self.commands_container.setObjectName(u"commands_container")
        sizePolicy.setHeightForWidth(self.commands_container.sizePolicy().hasHeightForWidth())
        self.commands_container.setSizePolicy(sizePolicy)
        self.gridLayout_6 = QGridLayout(self.commands_container)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.command_tree_collapse_button = QPushButton(self.commands_container)
        self.command_tree_collapse_button.setObjectName(u"command_tree_collapse_button")
        sizePolicy2.setHeightForWidth(self.command_tree_collapse_button.sizePolicy().hasHeightForWidth())
        self.command_tree_collapse_button.setSizePolicy(sizePolicy2)
        self.command_tree_collapse_button.setMaximumSize(QSize(150, 16777215))

        self.gridLayout_6.addWidget(self.command_tree_collapse_button, 0, 0, 1, 1)

        self.tab_2_command_tree_label = QLabel(self.commands_container)
        self.tab_2_command_tree_label.setObjectName(u"tab_2_command_tree_label")
        sizePolicy2.setHeightForWidth(self.tab_2_command_tree_label.sizePolicy().hasHeightForWidth())
        self.tab_2_command_tree_label.setSizePolicy(sizePolicy2)
        self.tab_2_command_tree_label.setMinimumSize(QSize(0, 25))
        self.tab_2_command_tree_label.setMaximumSize(QSize(200, 16777215))
        self.tab_2_command_tree_label.setAlignment(Qt.AlignCenter)

        self.gridLayout_6.addWidget(self.tab_2_command_tree_label, 0, 1, 1, 1)

        self.new_cmd_button = QPushButton(self.commands_container)
        self.new_cmd_button.setObjectName(u"new_cmd_button")
        sizePolicy1.setHeightForWidth(self.new_cmd_button.sizePolicy().hasHeightForWidth())
        self.new_cmd_button.setSizePolicy(sizePolicy1)
        self.new_cmd_button.setMinimumSize(QSize(0, 0))

        self.gridLayout_6.addWidget(self.new_cmd_button, 2, 0, 1, 1)

        self.edit_cmd_button = QPushButton(self.commands_container)
        self.edit_cmd_button.setObjectName(u"edit_cmd_button")
        sizePolicy1.setHeightForWidth(self.edit_cmd_button.sizePolicy().hasHeightForWidth())
        self.edit_cmd_button.setSizePolicy(sizePolicy1)
        self.edit_cmd_button.setMinimumSize(QSize(0, 0))

        self.gridLayout_6.addWidget(self.edit_cmd_button, 2, 1, 1, 1)

        self.delete_cmd_button = QPushButton(self.commands_container)
        self.delete_cmd_button.setObjectName(u"delete_cmd_button")
        sizePolicy1.setHeightForWidth(self.delete_cmd_button.sizePolicy().hasHeightForWidth())
        self.delete_cmd_button.setSizePolicy(sizePolicy1)

        self.gridLayout_6.addWidget(self.delete_cmd_button, 2, 2, 1, 1)

        self.command_tree = QTreeWidget(self.commands_container)
        __qtreewidgetitem2 = QTreeWidgetItem()
        __qtreewidgetitem2.setText(0, u"1");
        self.command_tree.setHeaderItem(__qtreewidgetitem2)
        self.command_tree.setObjectName(u"command_tree")
        sizePolicy.setHeightForWidth(self.command_tree.sizePolicy().hasHeightForWidth())
        self.command_tree.setSizePolicy(sizePolicy)
        self.command_tree.setMinimumSize(QSize(0, 0))
        self.command_tree.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.command_tree.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.command_tree.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

        self.gridLayout_6.addWidget(self.command_tree, 1, 0, 1, 3)

        self.splitter.addWidget(self.commands_container)
        self.commands_code_preview_container = QWidget(self.splitter)
        self.commands_code_preview_container.setObjectName(u"commands_code_preview_container")
        sizePolicy.setHeightForWidth(self.commands_code_preview_container.sizePolicy().hasHeightForWidth())
        self.commands_code_preview_container.setSizePolicy(sizePolicy)
        self.gridLayout_7 = QGridLayout(self.commands_code_preview_container)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.tab_2_code_preview_label = QLabel(self.commands_code_preview_container)
        self.tab_2_code_preview_label.setObjectName(u"tab_2_code_preview_label")
        sizePolicy2.setHeightForWidth(self.tab_2_code_preview_label.sizePolicy().hasHeightForWidth())
        self.tab_2_code_preview_label.setSizePolicy(sizePolicy2)
        self.tab_2_code_preview_label.setAlignment(Qt.AlignCenter)

        self.gridLayout_7.addWidget(self.tab_2_code_preview_label, 0, 0, 1, 1)

        self.codePreview_2 = QTreeWidget(self.commands_code_preview_container)
        __qtreewidgetitem3 = QTreeWidgetItem()
        __qtreewidgetitem3.setText(0, u"1");
        self.codePreview_2.setHeaderItem(__qtreewidgetitem3)
        self.codePreview_2.setObjectName(u"codePreview_2")
        sizePolicy.setHeightForWidth(self.codePreview_2.sizePolicy().hasHeightForWidth())
        self.codePreview_2.setSizePolicy(sizePolicy)
        self.codePreview_2.setMinimumSize(QSize(0, 0))
        self.codePreview_2.setMouseTracking(False)
        self.codePreview_2.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

        self.gridLayout_7.addWidget(self.codePreview_2, 1, 0, 1, 1)

        self.splitter.addWidget(self.commands_code_preview_container)

        self.gridLayout_5.addWidget(self.splitter, 0, 0, 1, 1)

        self.tabWidget.addTab(self.command_tab, "")

        self.gridLayout_4.addWidget(self.tabWidget, 0, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1460, 22))
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        self.menuHelp = QMenu(self.menubar)
        self.menuHelp.setObjectName(u"menuHelp")
        self.menuGenerate = QMenu(self.menubar)
        self.menuGenerate.setObjectName(u"menuGenerate")
        self.menuLog = QMenu(self.menubar)
        self.menuLog.setObjectName(u"menuLog")
        MainWindow.setMenuBar(self.menubar)
        QWidget.setTabOrder(self.command_tree_collapse_button, self.command_tree)
        QWidget.setTabOrder(self.command_tree, self.codePreview_2)
        QWidget.setTabOrder(self.codePreview_2, self.new_cmd_button)
        QWidget.setTabOrder(self.new_cmd_button, self.edit_cmd_button)
        QWidget.setTabOrder(self.edit_cmd_button, self.delete_cmd_button)
        QWidget.setTabOrder(self.delete_cmd_button, self.settings_tree)
        QWidget.setTabOrder(self.settings_tree, self.codePreview_1)
        QWidget.setTabOrder(self.codePreview_1, self.edit_setting_button)
        QWidget.setTabOrder(self.edit_setting_button, self.clear_setting_button)
        QWidget.setTabOrder(self.clear_setting_button, self.default_setting_button)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuLog.menuAction())
        self.menubar.addAction(self.menuGenerate.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addAction(self.actionSave_As)
        self.menuFile.addAction(self.actionPreferences)
        self.menuFile.addAction(self.actionExit)
        self.menuHelp.addAction(self.actionInputHandler_Documentation)
        self.menuHelp.addAction(self.actionAbout)
        self.menuGenerate.addAction(self.actionGenerate_CLI_Files)
        self.menuLog.addAction(self.actionOpen_Log_History)

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"InputHandler CLI generation tool", None))
        self.actionOpen.setText(QCoreApplication.translate("MainWindow", u"Open", None))
#if QT_CONFIG(shortcut)
        self.actionOpen.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+O", None))
#endif // QT_CONFIG(shortcut)
        self.actionSave.setText(QCoreApplication.translate("MainWindow", u"Save", None))
#if QT_CONFIG(shortcut)
        self.actionSave.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+S", None))
#endif // QT_CONFIG(shortcut)
        self.actionPreferences.setText(QCoreApplication.translate("MainWindow", u"Preferences", None))
#if QT_CONFIG(shortcut)
        self.actionPreferences.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+P", None))
#endif // QT_CONFIG(shortcut)
        self.actionInputHandler_Documentation.setText(QCoreApplication.translate("MainWindow", u"InputHandler Documentation", None))
#if QT_CONFIG(shortcut)
        self.actionInputHandler_Documentation.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+D", None))
#endif // QT_CONFIG(shortcut)
        self.actionAbout.setText(QCoreApplication.translate("MainWindow", u"About", None))
        self.actionGenerate_CLI_Files.setText(QCoreApplication.translate("MainWindow", u"Generate CLI Files", None))
#if QT_CONFIG(shortcut)
        self.actionGenerate_CLI_Files.setShortcut(QCoreApplication.translate("MainWindow", u"F2", None))
#endif // QT_CONFIG(shortcut)
        self.actionSave_As.setText(QCoreApplication.translate("MainWindow", u"Save As", None))
#if QT_CONFIG(shortcut)
        self.actionSave_As.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+Shift+S", None))
#endif // QT_CONFIG(shortcut)
        self.actionExit.setText(QCoreApplication.translate("MainWindow", u"Exit", None))
#if QT_CONFIG(shortcut)
        self.actionExit.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+X", None))
#endif // QT_CONFIG(shortcut)
        self.actionOpen_Log_History.setText(QCoreApplication.translate("MainWindow", u"Open Log History", None))
#if QT_CONFIG(shortcut)
        self.actionOpen_Log_History.setShortcut(QCoreApplication.translate("MainWindow", u"F1", None))
#endif // QT_CONFIG(shortcut)
        self.clear_setting_button.setText(QCoreApplication.translate("MainWindow", u"Clear", None))
        self.edit_setting_button.setText(QCoreApplication.translate("MainWindow", u"Edit", None))
        self.default_setting_button.setText(QCoreApplication.translate("MainWindow", u"Default", None))
        self.settings_tree_collapse_button.setText("")
        self.tab_1_settings_table_label.setText(QCoreApplication.translate("MainWindow", u"Settings", None))
        self.tab_1_code_preview_label.setText(QCoreApplication.translate("MainWindow", u"Code Preview", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.ih_settings_tab), QCoreApplication.translate("MainWindow", u"  InputHandler Settings  ", None))
#if QT_CONFIG(tooltip)
        self.command_tree_collapse_button.setToolTip(QCoreApplication.translate("MainWindow", u"open command settings menu", None))
#endif // QT_CONFIG(tooltip)
        self.command_tree_collapse_button.setText("")
        self.tab_2_command_tree_label.setText(QCoreApplication.translate("MainWindow", u"Commands", None))
        self.new_cmd_button.setText(QCoreApplication.translate("MainWindow", u"New", None))
        self.edit_cmd_button.setText(QCoreApplication.translate("MainWindow", u"Edit", None))
        self.delete_cmd_button.setText(QCoreApplication.translate("MainWindow", u"Delete", None))
        self.tab_2_code_preview_label.setText(QCoreApplication.translate("MainWindow", u"Code Preview", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.command_tab), QCoreApplication.translate("MainWindow", u"  Command Tree  ", None))
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"  File  ", None))
        self.menuHelp.setTitle(QCoreApplication.translate("MainWindow", u"Help", None))
        self.menuGenerate.setTitle(QCoreApplication.translate("MainWindow", u"Generate", None))
        self.menuLog.setTitle(QCoreApplication.translate("MainWindow", u"Log", None))
    # retranslateUi

