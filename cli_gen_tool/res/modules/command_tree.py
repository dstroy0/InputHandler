##
# @file command_tree.py
# @author Douglas Quigg (dstroy0 dquigg123@gmail.com)
# @brief MainWindow external methods
# @version 1.0
# @date 2022-07-30
# @copyright Copyright (c) 2022
# Copyright (C) 2022 Douglas Quigg (dstroy0) <dquigg123@gmail.com>
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# version 3 as published by the Free Software Foundation.

from __future__ import absolute_import

from PySide6.QtWidgets import QTableView, QTreeWidgetItem, QHeaderView
from PySide6.QtCore import QAbstractTableModel, QModelIndex, Qt

from res.modules.logging_setup import Logger

class CommandParametersTableViewModel(QAbstractTableModel):
    def __init__(self, parameters=None) -> None:
        super().__init__()
        self.parameters = parameters
        self.keys = list(parameters.keys())
        self.values = list(parameters.values())
        print(parameters)
        self.gen_table(parameters)
    
    def gen_table(self, parameters):        
        self.column_count = 4
        self.row_count = 4
        if len(parameters["commandArguments"]) > 1:
            # has arguments
            self.row_count = self.row_count + (len(parameters["commandArguments"]) % 4)        

    def columnCount(self, parent=QModelIndex()) -> int:
        return self.column_count

    def rowCount(self, parent=QModelIndex()) -> int:
        return self.row_count

    def data(self, index, role):
        if role == Qt.DisplayRole:            
            mIndex = ((index.row() - 1) * self.column_count) + index.column()
            ret = ""
            if mIndex < len(self.keys):
                ret = str(self.keys[mIndex]) + ":" + str(self.values[mIndex])
            return ret        
    
# command_tree methods
class CommandTreeMethods(object):    
    def __init__(self) -> None:
        super(CommandTreeMethods,self).__init__()
        CommandTreeMethods.logger = Logger.get_child_logger(self.logger, __name__)        
        
    def add_qtreewidgetitem(self, parent, dict_index=None) -> None:                
        if dict_index == None:
            dict_index = str(self.cliOpt["var"]["num_commands"])

        command_parameters = self.cliOpt["commands"]["parameters"][dict_index]        
        self.cliOpt["commands"]["QTreeWidgetItem"][dict_index] = QTreeWidgetItem(parent, [command_parameters["commandString"],""])
        tree_item = self.cliOpt["commands"]["QTreeWidgetItem"][dict_index]        
        tree_item.setFlags(tree_item.flags() | Qt.ItemIsEditable)
        tree_item.setFirstColumnSpanned(True)
        self.build_command_parameters_table_view(dict_index, tree_item, command_parameters)
        
    def rem_qtreewidgetitem(self, dict_pos):
        self.ui.command_tree.removeItemWidget(self.cliOpt["commands"]["QTreeWidgetItem"][dict_pos[2]],0)        
        if dict_pos[2] in self.cliOpt["commands"]["QTableView"]["models"]:
            del self.cliOpt["commands"]["QTableView"]["models"][dict_pos[2]]
        if dict_pos[2] in self.cliOpt["commands"]["QTableView"]:
            del self.cliOpt["commands"]["QTableView"][dict_pos[2]]
        if dict_pos[2] in self.cliOpt["commands"]["parameters"]:
            del self.cliOpt["commands"]["parameters"][dict_pos[2]]
        if dict_pos[2] in self.cliOpt["commands"]["QTreeWidgetItem"]:
            del self.cliOpt["commands"]["QTreeWidgetItem"][dict_pos[2]]
        
        
    def build_command_parameters_table_view(self, dict_index, tree_item, command_parameters):                
        command_tree = self.ui.command_tree        
        tree_item = self.cliOpt["commands"]["QTreeWidgetItem"][dict_index]
        self.cliOpt["commands"]["QTableView"]["models"][dict_index] = CommandParametersTableViewModel(command_parameters)
        self.cliOpt["commands"]["QTableView"][dict_index] = QTableView()
        table_view = self.cliOpt["commands"]["QTableView"][dict_index]
        table_view.setModel(self.cliOpt["commands"]["QTableView"]["models"][dict_index])                
        command_tree.setItemWidget(tree_item,0,table_view)
            
        
    def build_command_tree(self):
        command_tree = self.ui.command_tree                
        command_tree.setHeaderLabels(["Command Tree",""])
        command_tree.header().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        command_tree.setColumnCount(2)
        command_tree.setColumnHidden(1,1) # dict positional data
                        
# end of file
