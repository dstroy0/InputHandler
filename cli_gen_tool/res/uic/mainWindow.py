# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainWindow.ui'
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
from PySide6.QtWidgets import (QAbstractScrollArea, QApplication, QGridLayout, QHeaderView,
    QLabel, QMainWindow, QMenu, QMenuBar,
    QPushButton, QSizePolicy, QTabWidget, QTreeWidget,
    QTreeWidgetItem, QVBoxLayout, QWidget)

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
        MainWindow.setMinimumSize(QSize(1460, 885))
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
        sizePolicy1 = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy1)
        self.centralwidget.setMinimumSize(QSize(1420, 850))
        self.centralwidget.setMouseTracking(False)
        self.centralwidget.setLayoutDirection(Qt.LeftToRight)
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        sizePolicy1.setHeightForWidth(self.tabWidget.sizePolicy().hasHeightForWidth())
        self.tabWidget.setSizePolicy(sizePolicy1)
        self.tabWidget.setMinimumSize(QSize(1420, 850))
        self.tabWidget.setSizeIncrement(QSize(0, 0))
        self.tabWidget.setMouseTracking(False)
        self.tabWidget.setAutoFillBackground(True)
        self.ih_settings_tab = QWidget()
        self.ih_settings_tab.setObjectName(u"ih_settings_tab")
        sizePolicy1.setHeightForWidth(self.ih_settings_tab.sizePolicy().hasHeightForWidth())
        self.ih_settings_tab.setSizePolicy(sizePolicy1)
        self.ih_settings_tab.setMouseTracking(False)
        self.gridLayout = QGridLayout(self.ih_settings_tab)
        self.gridLayout.setObjectName(u"gridLayout")
        self.tab_1_code_preview_label = QLabel(self.ih_settings_tab)
        self.tab_1_code_preview_label.setObjectName(u"tab_1_code_preview_label")
        self.tab_1_code_preview_label.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.tab_1_code_preview_label, 0, 3, 1, 1)

        self.settings_tree = QTreeWidget(self.ih_settings_tab)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setText(0, u"1");
        self.settings_tree.setHeaderItem(__qtreewidgetitem)
        self.settings_tree.setObjectName(u"settings_tree")
        sizePolicy1.setHeightForWidth(self.settings_tree.sizePolicy().hasHeightForWidth())
        self.settings_tree.setSizePolicy(sizePolicy1)
        self.settings_tree.setMinimumSize(QSize(800, 200))
        self.settings_tree.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.settings_tree.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.settings_tree.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

        self.gridLayout.addWidget(self.settings_tree, 1, 0, 1, 3)

        self.editButton_1 = QPushButton(self.ih_settings_tab)
        self.editButton_1.setObjectName(u"editButton_1")
        sizePolicy2 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.editButton_1.sizePolicy().hasHeightForWidth())
        self.editButton_1.setSizePolicy(sizePolicy2)

        self.gridLayout.addWidget(self.editButton_1, 2, 0, 1, 1)

        self.clearButton_1 = QPushButton(self.ih_settings_tab)
        self.clearButton_1.setObjectName(u"clearButton_1")
        sizePolicy2.setHeightForWidth(self.clearButton_1.sizePolicy().hasHeightForWidth())
        self.clearButton_1.setSizePolicy(sizePolicy2)

        self.gridLayout.addWidget(self.clearButton_1, 2, 1, 1, 1)

        self.defaultButton_1 = QPushButton(self.ih_settings_tab)
        self.defaultButton_1.setObjectName(u"defaultButton_1")
        sizePolicy2.setHeightForWidth(self.defaultButton_1.sizePolicy().hasHeightForWidth())
        self.defaultButton_1.setSizePolicy(sizePolicy2)

        self.gridLayout.addWidget(self.defaultButton_1, 2, 2, 1, 1)

        self.tab_1_settings_table_label = QLabel(self.ih_settings_tab)
        self.tab_1_settings_table_label.setObjectName(u"tab_1_settings_table_label")
        self.tab_1_settings_table_label.setMinimumSize(QSize(0, 25))
        self.tab_1_settings_table_label.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.tab_1_settings_table_label, 0, 0, 1, 3)

        self.codePreview_1 = QTreeWidget(self.ih_settings_tab)
        __qtreewidgetitem1 = QTreeWidgetItem()
        __qtreewidgetitem1.setText(0, u"1");
        self.codePreview_1.setHeaderItem(__qtreewidgetitem1)
        self.codePreview_1.setObjectName(u"codePreview_1")
        sizePolicy.setHeightForWidth(self.codePreview_1.sizePolicy().hasHeightForWidth())
        self.codePreview_1.setSizePolicy(sizePolicy)
        self.codePreview_1.setMinimumSize(QSize(600, 200))
        self.codePreview_1.setMouseTracking(False)
        self.codePreview_1.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.codePreview_1.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.codePreview_1.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

        self.gridLayout.addWidget(self.codePreview_1, 1, 3, 2, 1)

        self.tabWidget.addTab(self.ih_settings_tab, "")
        self.command_tab = QWidget()
        self.command_tab.setObjectName(u"command_tab")
        sizePolicy1.setHeightForWidth(self.command_tab.sizePolicy().hasHeightForWidth())
        self.command_tab.setSizePolicy(sizePolicy1)
        self.command_tab.setMouseTracking(False)
        self.command_tab.setLayoutDirection(Qt.LeftToRight)
        self.gridLayout_2 = QGridLayout(self.command_tab)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.openCloseSettingsMenuButton = QPushButton(self.command_tab)
        self.openCloseSettingsMenuButton.setObjectName(u"openCloseSettingsMenuButton")
        self.openCloseSettingsMenuButton.setMaximumSize(QSize(150, 16777215))

        self.gridLayout_2.addWidget(self.openCloseSettingsMenuButton, 0, 0, 1, 1)

        self.newButton_2 = QPushButton(self.command_tab)
        self.newButton_2.setObjectName(u"newButton_2")
        self.newButton_2.setMinimumSize(QSize(265, 0))

        self.gridLayout_2.addWidget(self.newButton_2, 3, 0, 1, 1)

        self.editButton_2 = QPushButton(self.command_tab)
        self.editButton_2.setObjectName(u"editButton_2")

        self.gridLayout_2.addWidget(self.editButton_2, 3, 1, 1, 1)

        self.tab_2_command_tree_label = QLabel(self.command_tab)
        self.tab_2_command_tree_label.setObjectName(u"tab_2_command_tree_label")
        self.tab_2_command_tree_label.setMinimumSize(QSize(0, 25))
        self.tab_2_command_tree_label.setMaximumSize(QSize(350, 16777215))
        self.tab_2_command_tree_label.setAlignment(Qt.AlignCenter)

        self.gridLayout_2.addWidget(self.tab_2_command_tree_label, 0, 1, 1, 1)

        self.deleteButton_2 = QPushButton(self.command_tab)
        self.deleteButton_2.setObjectName(u"deleteButton_2")

        self.gridLayout_2.addWidget(self.deleteButton_2, 3, 2, 1, 1)

        self.tab_2_code_preview_label = QLabel(self.command_tab)
        self.tab_2_code_preview_label.setObjectName(u"tab_2_code_preview_label")
        self.tab_2_code_preview_label.setAlignment(Qt.AlignCenter)

        self.gridLayout_2.addWidget(self.tab_2_code_preview_label, 0, 3, 1, 1)

        self.command_tree = QTreeWidget(self.command_tab)
        __qtreewidgetitem2 = QTreeWidgetItem()
        __qtreewidgetitem2.setText(0, u"1");
        self.command_tree.setHeaderItem(__qtreewidgetitem2)
        self.command_tree.setObjectName(u"command_tree")
        sizePolicy1.setHeightForWidth(self.command_tree.sizePolicy().hasHeightForWidth())
        self.command_tree.setSizePolicy(sizePolicy1)
        self.command_tree.setMinimumSize(QSize(800, 200))
        self.command_tree.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.command_tree.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.command_tree.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

        self.gridLayout_2.addWidget(self.command_tree, 1, 0, 1, 3)

        self.codePreview_2 = QTreeWidget(self.command_tab)
        __qtreewidgetitem3 = QTreeWidgetItem()
        __qtreewidgetitem3.setText(0, u"1");
        self.codePreview_2.setHeaderItem(__qtreewidgetitem3)
        self.codePreview_2.setObjectName(u"codePreview_2")
        sizePolicy1.setHeightForWidth(self.codePreview_2.sizePolicy().hasHeightForWidth())
        self.codePreview_2.setSizePolicy(sizePolicy1)
        self.codePreview_2.setMinimumSize(QSize(600, 200))
        self.codePreview_2.setMouseTracking(False)
        self.codePreview_2.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

        self.gridLayout_2.addWidget(self.codePreview_2, 1, 3, 3, 1)

        self.tabWidget.addTab(self.command_tab, "")

        self.verticalLayout.addWidget(self.tabWidget)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1460, 21))
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        self.menuHelp = QMenu(self.menubar)
        self.menuHelp.setObjectName(u"menuHelp")
        self.menuGenerate = QMenu(self.menubar)
        self.menuGenerate.setObjectName(u"menuGenerate")
        self.menuLog = QMenu(self.menubar)
        self.menuLog.setObjectName(u"menuLog")
        MainWindow.setMenuBar(self.menubar)
        QWidget.setTabOrder(self.openCloseSettingsMenuButton, self.command_tree)
        QWidget.setTabOrder(self.command_tree, self.codePreview_2)
        QWidget.setTabOrder(self.codePreview_2, self.newButton_2)
        QWidget.setTabOrder(self.newButton_2, self.editButton_2)
        QWidget.setTabOrder(self.editButton_2, self.deleteButton_2)
        QWidget.setTabOrder(self.deleteButton_2, self.tabWidget)
        QWidget.setTabOrder(self.tabWidget, self.settings_tree)
        QWidget.setTabOrder(self.settings_tree, self.codePreview_1)
        QWidget.setTabOrder(self.codePreview_1, self.editButton_1)
        QWidget.setTabOrder(self.editButton_1, self.clearButton_1)
        QWidget.setTabOrder(self.clearButton_1, self.defaultButton_1)

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
        self.tab_1_code_preview_label.setText(QCoreApplication.translate("MainWindow", u"Code Preview", None))
        self.editButton_1.setText(QCoreApplication.translate("MainWindow", u"Edit", None))
        self.clearButton_1.setText(QCoreApplication.translate("MainWindow", u"Clear", None))
        self.defaultButton_1.setText(QCoreApplication.translate("MainWindow", u"Default", None))
        self.tab_1_settings_table_label.setText(QCoreApplication.translate("MainWindow", u"Settings               ", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.ih_settings_tab), QCoreApplication.translate("MainWindow", u"InputHandler Settings", None))
#if QT_CONFIG(tooltip)
        self.openCloseSettingsMenuButton.setToolTip(QCoreApplication.translate("MainWindow", u"open command settings menu", None))
#endif // QT_CONFIG(tooltip)
        self.openCloseSettingsMenuButton.setText(QCoreApplication.translate("MainWindow", u"Command settings menu", None))
        self.newButton_2.setText(QCoreApplication.translate("MainWindow", u"New", None))
        self.editButton_2.setText(QCoreApplication.translate("MainWindow", u"Edit", None))
        self.tab_2_command_tree_label.setText(QCoreApplication.translate("MainWindow", u"                          Commands", None))
        self.deleteButton_2.setText(QCoreApplication.translate("MainWindow", u"Delete", None))
        self.tab_2_code_preview_label.setText(QCoreApplication.translate("MainWindow", u"Code Preview", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.command_tab), QCoreApplication.translate("MainWindow", u"Command Tree", None))
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
        self.menuHelp.setTitle(QCoreApplication.translate("MainWindow", u"Help", None))
        self.menuGenerate.setTitle(QCoreApplication.translate("MainWindow", u"Generate", None))
        self.menuLog.setTitle(QCoreApplication.translate("MainWindow", u"Log", None))
    # retranslateUi

