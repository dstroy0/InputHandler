##
# @file cli_gen_tool.py
# @author Douglas Quigg (dstroy0 dquigg123@gmail.com)
# @brief InputHandler CLI generation tool
# @version 0.1
# @date 2022-06-10
# @copyright Copyright (c) 2022
from __future__ import absolute_import # easy import pathing
version = 0.1 # save serialization
# Copyright (C) 2022 Douglas Quigg (dstroy0) <dquigg123@gmail.com>

# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# version 3 as published by the Free Software Foundation.

# imports
import os
import sys
import json
import platform
from PySide6.QtWidgets import (QApplication, QMainWindow, QDialog, QLabel,
                               QVBoxLayout, QFileDialog, QHeaderView, QDialogButtonBox,
                               QTreeWidgetItem, QStyle)
from PySide6.QtCore import (QFile, Qt, QIODevice, QTextStream,
                            QByteArray, QDir, QRegularExpression)
from PySide6.QtGui import(QRegularExpressionValidator)

# import classes generated by PySide6 uic
from res.uic.mainWindow import Ui_MainWindow # main window with tabs
from res.uic.commandParametersDialog import Ui_commandParametersDialog # tab two popup dialog box

# MainWindow is the parent of all process subwindows (MainWindow is noninteractable when popup is active)
class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        # init popup dialog    
        self.ui.commandParameters = QDialog(self)               
        self.ui.commandParameters.dlg = Ui_commandParametersDialog()
        self.ui.commandParameters.dlg.setupUi(self.ui.commandParameters)        
        self.ui.commandParameters.setMaximumSize(0,0)            
        
        # MainWindow var
        
        # icons
        pixmapapi = QStyle.StandardPixmap.SP_FileDialogContentsView
        icon = self.style().standardIcon(pixmapapi)        
        self.ui.fileDialogContentsViewIcon = icon
        
        # session db
        self.session = {}
        # active save filename
        self.saveFileName = ''

        # self.cfgFileLines = []
        
        # cli opt db
        self.cliOpt = {'var': {'num_commands': 0,
                               'tool_version':str(version)},
                       'commands': {},
                       'config':{'file_lines':[],
                                 'tree':{'root':{},
                                         'parents':{},
                                         'items':{'library settings':{},
                                                  'progmem settings':{},                            
                                                  'debug methods':{},
                                                  'optional methods':{}}}}}
        
        # temp for testing
        self.parse_config_header_file()
        
        # command parameters dict keys list
        self.commandParametersKeys = ['functionName',
                                      'commandString',
                                      'commandLength',
                                      'parentId',
                                      'commandId',
                                      'commandHasWildcards',
                                      'commandDepth',
                                      'commandSubcommands',
                                      'commandArgumentHandling',
                                      'commandMinArgs',
                                      'commandMaxArgs',
                                      'commandArguments']

        # default settings dict to regen cli_gen_tool.json if it becomes corrupt
        self.defaultGuiOpt = {"tool_version":str(version),
                              "opt": { "save_filename": None,
                                       "recent_files": {},
                                       "config_file": "default",
                                       "output_dir": "output/",
                                       "window_size": "default"}}
        # end MainWindow var
        
        # MainWindow objects
        
        # actions setup
        # file menu
        self.ui.actionOpen.triggered.connect(self.open_file)
        self.ui.actionSave.triggered.connect(self.save_file)
        self.ui.actionSave_As.triggered.connect(self.save_file_as)
        self.ui.actionPreferences.triggered.connect(self.gui_settings)
        self.ui.actionExit.triggered.connect(self.gui_exit)
        # generate menu
        self.ui.actionGenerate_CLI_Files.triggered.connect(self.generate_cli_files)
        # about menu
        self.ui.actionAbout.triggered.connect(self.gui_about)
        self.ui.actionInputHandler_Documentation.triggered.connect(self.gui_documentation)
        
        # buttons setup
        # tab 1
        self.ui.editButton_1.clicked.connect(self.clicked_edit_tab_one)
        self.ui.clearButton_1.clicked.connect(self.clicked_clear_tab_one)
        self.ui.defaultButton_1.clicked.connect(self.clicked_default_tab_one)
        # tab 2
        # always visible
        self.ui.newButton_2.clicked.connect(self.clicked_new_tab_two)
        self.ui.editButton_2.clicked.connect(self.clicked_edit_tab_two)
        self.ui.deleteButton_2.clicked.connect(self.clicked_delete_tab_two)
        self.ui.openCloseSettingsMenuButton.clicked.connect(self.clicked_open_command_settings_menu_tab_two)
        
        # change driven events
        # tab 2
        self.ui.commandParameters.dlg.commandString.textChanged.connect(self.command_string_text_changed)
        
        # tab 1
        # settings_tree widget setup
        settings_tree = self.ui.settings_tree
        settings_tree.setHeaderLabels(("Section","Macro Name", "Type", "Value"))
        settings_tree.header().setSectionResizeMode(0, QHeaderView.Stretch)        
        settings_tree.header().setSectionResizeMode(1, QHeaderView.Stretch)
        settings_tree.header().setSectionResizeMode(3, QHeaderView.Stretch)
        settings_tree.setColumnCount(4)        
        
        tree = (self.cliOpt['config']['tree'])                    
        cfg_dict = (self.cliOpt['config']['tree']['items'])
        
        tree.update({'root':QTreeWidgetItem(settings_tree, ["src/config/config.h",""])})
        tree['root'].setIcon(0, self.ui.fileDialogContentsViewIcon)
               
        # make the parents children of root using the keys from 'cfg_dict'
        for key in cfg_dict:
            tree['parents'].update({key:QTreeWidgetItem(tree['root'], [key,'','',''])})
            
        # build tree                
        for key in cfg_dict:
            for item in cfg_dict[key]:
                regexp = QRegularExpression("(\s*[\/][\/]\s*)")
                sub_dict = (cfg_dict[key][item]['fields'])
                match = regexp.match(sub_dict[1])
                # sort out boolean fields
                if match.hasMatch() and (sub_dict[0] >= 71):                    
                    sub_dict.update({4:False})                    
                    item_list = ['line : '+str(sub_dict[0]),sub_dict[3].strip(),"True/False",str(sub_dict[4])]                    
                    sub_dict.update({5:QTreeWidgetItem(tree['parents'][key], item_list)})
                    sub_dict[5].setFlags(sub_dict[5].flags() | Qt.ItemIsEditable)
                elif not match.hasMatch() and (sub_dict[0] >= 71):
                    sub_dict.update({4:True})                    
                    item_list = ['line : '+str(sub_dict[0]),sub_dict[3].strip(),"True/False",str(sub_dict[4])]
                    sub_dict.update({5:QTreeWidgetItem(tree['parents'][key], item_list)})
                    sub_dict[5].setFlags(sub_dict[5].flags() | Qt.ItemIsEditable)
                else:
                    number_field = int(sub_dict[4])
                    if number_field <= 255:
                        type_field = "uint8_t" 
                    elif number_field > 255 and number_field <= 65535:
                        type_field = "uint16_t"                    
                    elif number_field > 65535:
                        type_field = "uin32_t"
                    item_list = ['line : '+str(sub_dict[0]),sub_dict[3].strip(),type_field,str(number_field)]
                    sub_dict.update({5:QTreeWidgetItem(tree['parents'][key], item_list)})
                    sub_dict[5].setFlags(sub_dict[5].flags() | Qt.ItemIsEditable)
    
        settings_tree.setEditTriggers(self.ui.settings_tree.NoEditTriggers)
        settings_tree.itemDoubleClicked.connect(self.check_if_col_editable)
        
        # print(json.dumps(self.cliOpt, indent=4, sort_keys=True, default=lambda o: ''))
        
        # tab 2        
        # command parameters dialog box setup
        self.ui.commandParameters.dlg.functionName.setValidator(self.regex_validator("^([a-zA-Z_])+$"))
        self.ui.commandParameters.dlg.commandString.setValidator(self.regex_validator("^([a-zA-Z_*])+$"))
        self.ui.commandParameters.dlg.commandParentId.setValidator(self.regex_validator("^([0-9])+$"))
        self.ui.commandParameters.dlg.commandId.setValidator(self.regex_validator("^([0-9])+$"))
    
        self.ui.commandParameters.dlg.commandDepth.setMaximum(255)
        self.ui.commandParameters.dlg.commandSubcommands.setMaximum(255)
    
        self.ui.commandParameters.dlg.commandMinArgs.setMaximum(255)
        self.ui.commandParameters.dlg.commandMaxArgs.setMaximum(255)
        
        self.ui.commandParameters.dlg.add8bituint.clicked.connect(self.csv_button)
        self.ui.commandParameters.dlg.add16bituint.clicked.connect(self.csv_button)
        self.ui.commandParameters.dlg.add32bituint.clicked.connect(self.csv_button)
        self.ui.commandParameters.dlg.add16bitint.clicked.connect(self.csv_button)
        self.ui.commandParameters.dlg.addfloat.clicked.connect(self.csv_button)
        self.ui.commandParameters.dlg.addchar.clicked.connect(self.csv_button)
        self.ui.commandParameters.dlg.addstartstop.clicked.connect(self.csv_button)
        self.ui.commandParameters.dlg.addnotype.clicked.connect(self.csv_button)
        self.ui.commandParameters.dlg.rem.clicked.connect(self.csv_button)
        self.ui.commandParameters.dlg.rem1.clicked.connect(self.csv_button)
        self.ui.commandParameters.dlg.rem2.clicked.connect(self.csv_button)
        self.ui.commandParameters.dlg.rem3.clicked.connect(self.csv_button)
        self.ui.commandParameters.dlg.rem4.clicked.connect(self.csv_button)
        self.ui.commandParameters.dlg.rem5.clicked.connect(self.csv_button)
        self.ui.commandParameters.dlg.rem6.clicked.connect(self.csv_button)
        self.ui.commandParameters.dlg.rem7.clicked.connect(self.csv_button)
    
        self.ui.commandParameters.dlg.buttonBox.button(QDialogButtonBox.Reset).clicked.connect(self.clicked_command_parameters_buttonbox_reset)
        self.ui.commandParameters.dlg.buttonBox.accepted.connect(self.clicked_command_parameters_buttonbox_ok)
        self.ui.commandParameters.dlg.buttonBox.rejected.connect(self.clicked_command_parameters_buttonbox_cancel)
    
        self.ui.commandParameters.dlg.commandArgumentHandling.currentIndexChanged.connect(self.argument_handling_changed)
        self.ui.commandParameters.dlg.argumentsPane.setEnabled(False)          

        # load cli_gen_tool (session) json
        self.load_cli_gen_tool_json()
        # end __init__
            
    # actions
    def open_file(self):
        print('open file')
        # inherit from parent QMainWindow (block main window interaction while dialog box is open)
        dlg = QFileDialog(self)
        dlg.setFileMode(QFileDialog.ExistingFile)
        dlg.setNameFilter("Settings json (*.json)")
        dlg.setViewMode(QFileDialog.Detail)
        fileName = ""
        if dlg.exec():
            fileName = dlg.selectedFiles()
        else:
            return  # dialog cancelled
        file = QFile(fileName[0])
        if (not file.open(QIODevice.ReadOnly | QIODevice.Text)):
            return  # TODO error
        data_in = QTextStream(file).readAll()
        file.close()
        self.cliOpt = json.loads(data_in)  # TODO try/except

    def save_file(self):
        print('save file')
        if self.saveFileName == '':
            self.save_file_as()
            return
        file = QFile(self.saveFileName)
        if (not file.open(QIODevice.WriteOnly | QIODevice.Text)):
            return  # TODO error
        out = QByteArray(json.dumps(self.cliOpt,
                         indent=4, sort_keys=True))  # dump pretty json
        file.write(out)
        file.close()

    def save_file_as(self):
        print('save file as')
        # inherit from parent QMainWindow (block main window interaction while dialog box is open)
        dlg = QFileDialog(self)
        fileName = dlg.getSaveFileName(self, "Save file name", "", ".json")
        if fileName[0] == '':
            return  # dialog cancelled
        fqname = fileName[0] + ".json"
        self.saveFileName = fqname
        file = QFile(fqname)
        if (not file.open(QIODevice.WriteOnly | QIODevice.Text)):
            return  # TODO error
        out = QByteArray(json.dumps(self.cliOpt, indent=4,
                         sort_keys=True))  # dump pretty json
        file.write(out)
        file.close()

    # TODO
    def gui_settings(self):
        print('preferences')

    # close gui
    def gui_exit(self):
        sys.exit(app.quit())

    # TODO
    # generate CLI files
    def generate_cli_files(self):
        print('generate cli files')

    def gui_about(self):
        # print('about')
        # inherit from parent QMainWindow (block main window interaction while dialog box is open)
        dlg = QDialog(self)
        dlg.layout = QVBoxLayout()
        dlg.setWindowTitle('About')
        dlg.git_link_label = QLabel()
        dlg.git_link_label.setText(
            "<a href=\"https://github.com/dstroy0/InputHandler\">Link to library git</a>")
        dlg.git_link_label.setAlignment(Qt.AlignCenter)
        dlg.git_link_label.setTextInteractionFlags(Qt.TextBrowserInteraction)
        dlg.git_link_label.setOpenExternalLinks(True)
        dlg.layout.addWidget(dlg.git_link_label)
        dlg.author_credit_label = QLabel()
        dlg.author_credit_label.setText(
            "Library authors:\nDouglas Quigg (dstroy0 dquigg123@gmail.com)\nBrendan Doherty (2bndy5 2bndy5@gmail.com)")
        dlg.author_credit_label.setAlignment(Qt.AlignCenter)
        dlg.layout.addWidget(dlg.author_credit_label)
        dlg.setLayout(dlg.layout)
        dlg.exec()

    def gui_documentation(self):
        os_type = platform.uname().system.lower()  # lowercase os type
        # windows
        if os_type == "windows":
            os.system("start \"\" https://dstroy0.github.io/InputHandler/")
        # macos
        elif os_type == "darwin":
            os.system("open \"\" https://dstroy0.github.io/InputHandler/")
        # linux
        elif os_type == "linux":
            os.system("xdg-open \"\" https://dstroy0.github.io/InputHandler/")

    # buttons
    # tab 1
    # TODO
    def clicked_edit_tab_one(self):
        print('clicked tab 1 edit')
    # TODO

    def clicked_clear_tab_one(self):
        print('clicked tab 1 clear')
    # TODO

    def clicked_default_tab_one(self):
        print('clicked tab 1 default')
    # tab 2
    # TODO

    def clicked_edit_tab_two(self):
        print('clicked tab 2 edit')
    # TODO

    def clicked_new_tab_two(self):
        print('clicked tab 2 new')
    # TODO

    def clicked_delete_tab_two(self):
        print('clicked tab 2 delete')

    def clicked_open_command_settings_menu_tab_two(self):
        print('clicked open/close command settings menu')        
        self.ui.commandParameters.exec()
        
    def clicked_close_command_settings_menu_tab_two(self):
        print('clicked close command settings menu')
        
    def clicked_command_parameters_buttonbox_ok(self):        
        print('ok')
        settings_to_validate = dict.fromkeys(self.commandParametersKeys, None)
        settings_to_validate['functionName'] = self.ui.commandParameters.dlg.functionName.text()
        settings_to_validate['commandString'] = self.ui.commandParameters.dlg.commandString.text()
        settings_to_validate['commandLength'] = len(settings_to_validate['commandString'])
        settings_to_validate['parentId'] = self.ui.commandParameters.dlg.commandParentId.text()
        settings_to_validate['commandId'] = self.ui.commandParameters.dlg.commandId.text()
        settings_to_validate['commandHasWildcards'] = self.ui.commandParameters.dlg.commandHasWildcards.isChecked()
        settings_to_validate['commandDepth'] = self.ui.commandParameters.dlg.commandDepth.text()
        settings_to_validate['commandSubcommands'] = self.ui.commandParameters.dlg.commandSubcommands.text()
        settings_to_validate['commandArgumentHandling'] = self.ui.commandParameters.dlg.commandArgumentHandling.currentIndex()
        settings_to_validate['commandMinArgs'] = self.ui.commandParameters.dlg.commandMinArgs.text()
        settings_to_validate['commandMaxArgs'] = self.ui.commandParameters.dlg.commandMaxArgs.text() 
        err = False
        if settings_to_validate['functionName'] == '':
            print('Function name cannot be empty')
            err = True
        if settings_to_validate['commandString'] == '':
            print('Command string cannot be empty')
            err = True
        if int(settings_to_validate['commandLength']) == 0:
            print('Command length cannot be zero')
            err = True
        if settings_to_validate['parentId'] == '' or int(settings_to_validate['parentId']) > 65535:
            print('Parent id cannot be greater than 65535')
            err = True
        if settings_to_validate['commandId'] == '' or int(settings_to_validate['commandId']) > 65535:
            print('Command id cannot be greater than 65535')
            err = True
        if settings_to_validate['commandDepth'] == '' or int(settings_to_validate['commandDepth']) > 255:
            print('Command depth cannot be greater than 255')
            err = True
        if settings_to_validate['commandSubcommands'] == '' or int(settings_to_validate['commandSubcommands']) > 255:
            print('Command cannot have more than 255 subcommands')
            err = True
        if int(settings_to_validate['commandArgumentHandling']) == 1 or 2:
            tmp = self.dict_from_csv_args()
            if settings_to_validate['commandArgumentHandling'] == 1:                
                # single argument                
                settings_to_validate['commandArguments'] = {0: tmp[0]}
            else:
                # argument array                
                settings_to_validate['commandArguments'] = tmp
        print(settings_to_validate)
        if err == True:
            return
        # get array index
        cmd_idx = self.cliOpt['var']['num_commands']
        # make dict from defined keys
        self.cliOpt['commands'][cmd_idx] = settings_to_validate
        print(self.cliOpt['commands'][cmd_idx])        
        
        # command parameters were accepted, so increment the array index
        self.cliOpt['var']['num_commands'] = self.cliOpt['var']['num_commands'] + 1
        # print object
        print(self.cliOpt['var'])
        self.ui.commandParameters.close()
    
    def clicked_command_parameters_buttonbox_reset(self):        
        print('reset')
        pre = self.ui.commandParameters.dlg
        pre.argumentsPlainTextCSV.clear()
        
    def clicked_command_parameters_buttonbox_cancel(self):        
        print('cancel')
        self.ui.commandParameters.close()
        
    def command_string_text_changed(self):
        self.ui.commandParameters.dlg.commandLengthLabel.setText(str(len(self.ui.commandParameters.dlg.commandString.text())))
    
    def argument_handling_changed(self):
        print('argument handling changed')
        if self.ui.commandParameters.dlg.commandArgumentHandling.currentIndex() != 0:
            self.ui.commandParameters.dlg.argumentsPane.setEnabled(True)
        else:
            self.ui.commandParameters.dlg.argumentsPane.setEnabled(False)
        
    def check_if_col_editable(self, item, column):
        # allow the third column to be editable
        if column == 3:
            self.ui.settings_tree.editItem(item, column)
            
    def parse_config_header_file(self):
        path = QDir()
        path.cdUp()
        config_path = path.currentPath() + "/src/config/config.h"    
        file = open(config_path, 'r')
        print("opened: ", config_path, sep='')
        self.cliOpt['config']['file_lines'] = file.readlines()
        file.close()
        
        debug_regexp = "(\s*[\/][\/]\s*)(\s*#define\s*)(DEBUG_\S*)"
        opt_method_regexp = "(\s*[\/]*\s*)(\s*#define\s*)(DISABLE_\S*)"
        setting_regexp = "(\s*[\/]*\s*)(\s*#define\s*)(?!\S*PGM_LEN)(UI_\S*\s*)(\d*)"
        progmem_regexp = "(\s*[\/]*\s*)(\s*#define\s*)(UI_\S*PGM_LEN\s*)(\d*)"        
        regexp_dict = {'library settings':setting_regexp,
                       'progmem settings':progmem_regexp,
                       'debug methods':debug_regexp,
                       'optional methods':opt_method_regexp                       
                      }                                     
        index = {'library settings':0,
                 'progmem settings':0,
                 'optional methods':0,
                 'debug methods':0
                }
        line_num = 0
        for line in self.cliOpt['config']['file_lines']:
            for key in regexp_dict:
                line_pos = 0
                regexp = QRegularExpression(regexp_dict[key])
                while line_pos != -1:
                    match = regexp.match(line, line_pos)
                    if match.hasMatch():
                        fields = {0:line_num}                        
                        for i in range(1,6):                            
                            if i < regexp.captureCount() + 1:
                                fields.update({i:match.captured(i)})
                            else:
                                fields.update({i:''})
                            
                        line_pos += match.capturedLength()                                                
                        entry = {index[key]:{'fields':fields}}
                        self.cliOpt['config']['tree']['items'][key].update(entry)
                        index[key] += 1   
                    else:
                        break
            line_num += 1
        # print(json.dumps(self.cliOpt['config']['tree']['items'], indent=4, sort_keys=True))
            
    def regex_validator(self, input):
        exp = QRegularExpression(input)
        return QRegularExpressionValidator(exp)       
    
    # TODO split this method
    def load_cli_gen_tool_json(self):        
        path = QDir.currentPath() + "/cli_gen_tool/cli_gen_tool.json"        
        file = QFile(path)
        if not file.exists():
            self.session = json.loads(self.defaultGuiOpt)
            print('cli_gen_tool.json doesn\'t exist, using default options')
            return
        if (not file.open(QIODevice.ReadOnly | QIODevice.Text)):
            file.close()
            file = QFile(path)
            print('cli_gen_tool/cli_gen_tool.json not found, attempting to create a new one.')            
            if (not file.open(QIODevice.WriteOnly | QIODevice.Text)):
                print('Unable to write new cli_gen_tool.json, please check permissions.')
                return
            out = QByteArray(json.dumps(self.defaultGuiOpt, indent=4, sort_keys=True))  # dump pretty json                        
            file.write(out)
            print('write successful')                        
            file.close()
            file = QFile(path)
            if (not file.open(QIODevice.ReadOnly | QIODevice.Text)):
                print('unable to open cli_gen_tool/cli_gen_tool.json')
        data_in = QTextStream(file).readAll()
        file.close()        
        # print(path)
        try:
            self.session = json.loads(data_in)
            print("cli_gen_tool.json:", self.session, sep='')
        except (ValueError, RuntimeError, TypeError, NameError) as e:
            print('json corrupt, removing')
            if self.json_except == 1:
                print('unable to read json, app exit')
                app.quit()
            self.json_except = 1
            os.remove(path) # delete corrupt json
            self.load_cli_gen_tool_json(self) # recurse to try and recreate cli_gen_tool.json
            print(e)
            
    def dict_from_csv_args(self):
        args_dict = {}
        args_list = []
        arg_num_list = []
        csv = self.ui.commandParameters.dlg.argumentsPlainTextCSV.toPlainText() + ','                   
        regexp = QRegularExpression("(\"(?:[^\"]|\")*\"|[^,\"\n\r]*)(,|\r?\n|\r)")        
        csv_pos = 0
        i = 0
        while csv_pos != -1:
            match = regexp.match(csv, csv_pos)            
            if match.hasMatch():                
                csv_pos += match.capturedLength()
                arg_num_list.append(i)
                i = i + 1
                args_list.append(match.captured().upper().strip(','))
            else:
                break                 
        args_dict = dict(zip(arg_num_list, args_list))        
        return args_dict

    def csv_button(self):
        # print button name
        print(self.sender().objectName())

# loop
if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())

# end of file
