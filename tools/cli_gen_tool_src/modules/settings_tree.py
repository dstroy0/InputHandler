##
# @file settings_tree.py
# @author Douglas Quigg (dstroy0 dquigg123@gmail.com)
# @brief MainWindow external methods
# @version 1.0
# @date 2022-07-08
# @copyright Copyright (c) 2022
# Copyright (C) 2022 Douglas Quigg (dstroy0) <dquigg123@gmail.com>
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# version 3 as published by the Free Software Foundation.

from __future__ import absolute_import

# imports
import copy
import json
from collections import OrderedDict

# pyside imports
from PySide6.QtCore import Qt, QAbstractTableModel, QModelIndex
from PySide6.QtWidgets import (
    QComboBox,
    QHeaderView,
    QAbstractItemView,
    QSizePolicy,
    QTreeWidget,
    QPushButton,
    QTreeWidgetItem,
    QTableView,
    QAbstractScrollArea,
    QHBoxLayout,
    QWidget,
    QStyle,
)

# external data models
from modules.data_models import dataModels
from modules.display_models import displayModels


class DelimitersTableViewModel(QAbstractTableModel):
    """Display model for a delimiters table

    Args:
        QAbstractTableModel (class): This class specializes QAbstractTableModel
    """

    def __init__(self, parent) -> None:

        super(DelimitersTableViewModel, self).__init__()
        self._parent = parent
        self.add_row_button = parent.add_row_button
        self.remove_row_buttons = parent.remove_row_buttons
        self.remove_row_button_icon = (
            QWidget().style().standardIcon(QStyle.StandardPixmap.SP_TrashIcon)
        )
        self.cliopt = parent.cliopt
        self.dict_pos = parent.dict_pos
        self.delimiters = parent.delimiters
        self.keys = list(self.delimiters.keys())
        self.values = list(self.delimiters.values())
        self.row_count = int(len(self.delimiters) + 1)
        self.column_count = 2
        self.editing = False
        self.clicked_row = None

        for i in range(self.row_count - 1):
            self.remove_row_buttons.append(QPushButton())
            self.remove_row_buttons[i].setIcon(self.remove_row_button_icon)

    def flags(self, index) -> Qt.ItemFlags:
        if (
            index.isValid()
            and index.column() == 0
            and index.row() < (self.rowCount() - 1)
        ):
            return (
                super().flags(index)
                | Qt.ItemIsSelectable
                | Qt.ItemIsEditable
                | Qt.ItemIsEnabled
            )
        else:
            return super().flags(index) | Qt.ItemIsSelectable | Qt.ItemIsEnabled

    def setData(self, index, value, role) -> bool:
        if role in (Qt.DisplayRole, Qt.EditRole):
            if not value:
                return False

            clean_value = value.strip("<>")
            if not clean_value:
                return False
            self.cliopt[self.dict_pos[0]]["var"][self.dict_pos[2]][
                str(index.row())
            ] = clean_value
            self.dataChanged.emit(index, index)
            table = self._parent.objectName().split(",")[2]
            self._parent.logger.info(
                f"{table} table, row {index.row()+1} data changed to <{clean_value}>"
            )
        return True

    def columnCount(self, parent: QModelIndex = None) -> int:
        return self.column_count

    def rowCount(self, parent: QModelIndex = None) -> int:
        return int(len(self.cliopt[self.dict_pos[0]]["var"][self.dict_pos[2]]) + 1)

    def ar(self) -> None:
        row = self.rowCount() - 1
        parent = self._parent.currentIndex()
        self.insertRow(row, parent)

    def insertRow(self, row: int, parent) -> bool:
        self.beginInsertRows(parent, row, row)
        start_len = len(self.cliopt[self.dict_pos[0]]["var"][self.dict_pos[2]])
        self.cliopt[self.dict_pos[0]]["var"][self.dict_pos[2]].update(
            {str(start_len): ""}
        )
        self.insertRows(row, 1, parent)
        self.endInsertRows()
        self.insert_row_move_buttons(row)
        self.dataChanged.emit(parent, parent)
        self.layoutChanged.emit()
        return super().insertRow(row, parent)

    def insert_row_move_buttons(self, row: int):
        self.remove_row_buttons.append(QPushButton())
        self.remove_row_buttons[row].setIcon(self.remove_row_button_icon)
        index = self.index(row, 0)
        self._parent.setIndexWidget(index, None)
        index = self.index(row, 1)
        self._parent.setIndexWidget(index, self.remove_row_buttons[row])
        self.remove_row_buttons[row].clicked.connect(self.rr)
        index = self.index(self.rowCount() - 1, 0)
        self.add_row_button = QPushButton("Add Delimiter")
        self.add_row_button.clicked.connect(self.ar)
        self._parent.setIndexWidget(index, self.add_row_button)

    def rr(self):
        row = self._parent.currentIndex().row()
        parent = self._parent.currentIndex()
        self.removeRow(row, parent)

    def removeRow(self, row: int = None, parent=None) -> bool:
        if not parent.isValid():
            row = self._parent.currentIndex().row()
            parent = self._parent.currentIndex()
        print(f"remove row {row}")

        self.beginRemoveRows(parent, row, row)
        del self.remove_row_buttons[row]
        del self.cliopt[self.dict_pos[0]]["var"][self.dict_pos[2]][str(row)]
        new_dict = copy.deepcopy(self.cliopt[self.dict_pos[0]]["var"][self.dict_pos[2]])

        self.cliopt[self.dict_pos[0]]["var"][self.dict_pos[2]] = {}

        i = 0
        for key in new_dict:
            self.cliopt[self.dict_pos[0]]["var"][self.dict_pos[2]].update(
                {str(i): new_dict[key]}
            )
            i += 1
        self.removeRows(row, row, parent)

        index = self.index(self.rowCount() - 1, 1)
        self._parent.setIndexWidget(index, None)
        index = self.index(self.rowCount() - 1, 0)
        self._parent.setIndexWidget(index, self.add_row_button)
        self.endRemoveRows()
        self.dataChanged.emit(parent, parent)
        self.layoutChanged.emit()
        return super().removeRow(row, parent)

    def moveRow(
        self,
        sourceParent: QModelIndex,
        sourceRow: int,
        destinationParent: QModelIndex,
        destinationChild: int,
    ) -> bool:
        self.beginMoveRows(
            QModelIndex(), sourceRow, sourceRow, QModelIndex(), destinationChild
        )

        self.endMoveRows()
        return super().moveRow(
            sourceParent, sourceRow, destinationParent, destinationChild
        )

    def data(self, index: QModelIndex, role: int):
        """Table data positioning.

        Args:
            index (QModelIndex): The model index.
            role (Qt Role): What role is the data.

        Returns:
            str: data in the cell
        """
        if not index.isValid():
            return None
        elif (
            index.column() == 0
            and (index.row() - 1)
            < (len(self.cliopt[self.dict_pos[0]]["var"][self.dict_pos[2]]) - 1)
            and role == Qt.DisplayRole
            or role == Qt.EditRole
        ):
            return (
                "<"
                + str(
                    self.cliopt[self.dict_pos[0]]["var"][self.dict_pos[2]][
                        str(index.row())
                    ]
                )
                + ">"
            )

        # returns tooltips on a valid index if there are any for the cell
        elif role == Qt.ToolTipRole:
            if (index.row() - 1) < (
                len(self.cliopt[self.dict_pos[0]]["var"][self.dict_pos[2]]) - 1
            ):
                if index.column() == 0:
                    return str(
                        f"type: {self.dict_pos[2]}, any char except the wildcard char is valid"
                    )
                else:
                    return str(f"remove row {index.row()+1}")
            else:
                if index.column() == 0:
                    return str(f"add row to {self.dict_pos[2]} table")
                else:
                    return None
        else:
            return None

    def headerData(self, section: int, orientation: int, role: int):
        if role == Qt.DisplayRole and orientation == Qt.Horizontal and section == 0:
            return "Delimiters"
        elif orientation == Qt.Vertical and role == Qt.DisplayRole:
            if int(section) < int(self.rowCount() - 1):
                return str(section + 1)
            else:
                return None
        else:
            return None

    def edit_table_view(self, index: QModelIndex):
        if index.isValid() and self.editing == False:
            self.editing = True
            self._parent.setCurrentIndex(index)
            self._parent.edit(index)


class DelimitersTableView(QTableView):
    def __init__(
        self,
        parent,
        logger,
        cursor,
        container,
        cliopt,
    ) -> None:
        super(DelimitersTableView, self).__init__()
        self.logger = logger
        self.cursor_ = cursor
        self.cliopt = cliopt
        self.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.dict_pos = container.data(4, 0).split(",")
        self.setObjectName(str(container.data(4, 0)))

        self.delimiters = cliopt[self.dict_pos[0]]["var"][self.dict_pos[2]]
        self.remove_row_buttons = []
        self.add_row_button = QPushButton("Add Delimiter")

        self.table_model = DelimitersTableViewModel(self)
        self.setModel(self.table_model)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.setSelectionMode(QAbstractItemView.SingleSelection)
        parent.setItemWidget(container, 0, self)

        index = self.table_model.index(self.table_model.rowCount() - 1, 0)
        self.setIndexWidget(index, self.add_row_button)

        for i in range(len(self.remove_row_buttons)):
            index = self.table_model.index(i, 1)
            self.setIndexWidget(index, self.remove_row_buttons[i])
            self.remove_row_buttons[i].clicked.connect(self.table_model.rr)

        self.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)

        self.add_row_button.clicked.connect(self.table_model.ar)
        self.clicked.connect(self.table_model.edit_table_view)
        self.clicked.connect(self.update_index)
        self.pressed.connect(self.table_model.edit_table_view)

    def update_index(self):
        self.setCurrentIndex(self.indexAt(self.cursor_pos()))

    def cursor_pos(self):
        return self.cursor_.pos()

    def dataChanged(self, topLeft, bottomRight, roles) -> None:
        if self.table_model.editing == True:
            self.table_model.editing = False
            print("edit complete")
        return super().dataChanged(topLeft, bottomRight, roles)


class SettingsTreeWidget(QTreeWidget):
    def __init__(self, parent, cliopt, session, logger) -> None:
        super(SettingsTreeWidget, self).__init__()
        self.command_tree = parent.command_tree
        self.update_code = parent.update_code
        self.loading = parent.loading
        self.setParent(parent.ui.settings_tree_container)
        self.items = []
        self.tables = []
        self.default_settings_tree_values = parent.default_settings_tree_values
        self._parent = parent
        self.cliopt = cliopt
        self.session = session
        self.item_clicked = None
        self._cursor = parent.qcursor
        self.logger = logger

        self.setHeaderLabel("Settings Tree")
        self.setColumnCount(5)
        self.setColumnHidden(4, 1)
        self.setHeaderLabels(("Section", "Macro Name", "Type", "Value"))
        self.header().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        for i in range(self.columnCount() - 1):
            self.header().setSectionResizeMode(i, QHeaderView.ResizeToContents)
            self.header().setSectionResizeMode(i, QHeaderView.Stretch)
        self.setMinimumWidth(400)
        self.setSelectionMode(QAbstractItemView.SingleSelection)

        # use the text in _tree for self.ui.settings_tree field labels, build the tree
        for parent in SettingsTreeMethods._tree:
            index_of_child = 0
            dict_key = parent

            is_config = True if dict_key == "config" else False
            # add parents to self.ui.settings_treeS

            if is_config:
                # make these parents children of root using the keys from 'cfg_dict'
                cfg_path = session["opt"]["input_config_file_path"]
                setting_container = QTreeWidgetItem(
                    self.invisibleRootItem(), ["Input config: " + cfg_path, ""]
                )
                setting_container.setIcon(0, self._parent.ui.fileDialogContentsViewIcon)
                setting_container.setToolTip(0, "Input config: " + cfg_path)

                for subsection in SettingsTreeMethods._tree["config"]:
                    # index_of_child = 0
                    setting_label = QTreeWidgetItem(
                        setting_container, [subsection, "", "", ""]
                    )
                    # make the treewidgetitem editable
                    setting_label.setFlags(setting_label.flags() | Qt.ItemIsSelectable)
                    # make the treewidgetitem span columns

                    for item in SettingsTreeMethods._tree["config"][subsection]:
                        # dict_pos = subsection + "," + str(index_of_child) + "," + item
                        var_initial_val = self.cliopt["config"]["var"][subsection][
                            item
                        ]["value"]
                        has_combobox = False
                        tooltip = SettingsTreeMethods._tree[dict_key][subsection][item][
                            "tooltip"
                        ]
                        combobox_tooltip = SettingsTreeMethods._tree[dict_key][
                            subsection
                        ][item]["tooltip"]
                        if (
                            SettingsTreeMethods._tree[dict_key][subsection][item][
                                "type"
                            ]
                            == "Enable/Disable"
                        ):
                            has_combobox = True
                            tooltip = ""
                        index_of_child = self.set_up_child(
                            subsection,
                            setting_label,
                            index_of_child,
                            item,
                            SettingsTreeMethods._tree[dict_key][subsection][item][
                                "type"
                            ],
                            tooltip,
                            var_initial_val,
                            has_combobox,
                            combobox_tooltip,
                        )
            elif not is_config:
                setting_container = QTreeWidgetItem(
                    self.invisibleRootItem(), [dict_key, ""]
                )
                setting_container.setIcon(0, self._parent.ui.commandLinkIcon)

                for child in SettingsTreeMethods._tree[parent]:

                    dict_pos = dict_key + "," + str(index_of_child) + "," + child

                    var_initial_val = self.cliopt[dict_key]["var"][child]
                    if (
                        child == "data delimiter sequences"
                        or child == "start stop data delimiter sequences"
                    ):
                        setting_label = QTreeWidgetItem(
                            setting_container, [child, "", "", ""]
                        )
                        setting_label.setData(4, 0, dict_pos)
                        # setting_label.setFlags(setting_label.flags() | Qt.ItemIsSelectable)
                        index_of_child = self.build_tree_table_widget(
                            setting_label, index_of_child, dict_pos
                        )
                    else:
                        has_combobox = False
                        tooltip = SettingsTreeMethods._tree[dict_key][child]["tooltip"]
                        combobox_tooltip = SettingsTreeMethods._tree[dict_key][child][
                            "tooltip"
                        ]
                        if (
                            SettingsTreeMethods._tree[dict_key][child]["type"]
                            == "Enable/Disable"
                        ):
                            has_combobox = True
                            tooltip = ""
                        index_of_child = self.set_up_child(
                            dict_key,
                            setting_container,
                            index_of_child,
                            child,
                            SettingsTreeMethods._tree[dict_key][child]["type"],
                            tooltip,
                            var_initial_val,
                            has_combobox,
                            combobox_tooltip,
                        )

                    self.default_settings_tree_values.update(
                        {str(child).strip(): var_initial_val}
                    )

        self.setEditTriggers(self.NoEditTriggers)
        # update cliopt with new value when editing is complete
        self.itemChanged.connect(self.settings_tree_edit_complete)
        # check if user clicked on the column we want them to edit
        self.itemDoubleClicked.connect(self.check_if_settings_tree_col_editable)
        # check if user hit enter on an item
        self.itemActivated.connect(self.settings_tree_item_activated)
        # self._parent.settings_tree_button_toggles()
        self.setSelectionMode(QAbstractItemView.SingleSelection)
        self.itemSelectionChanged.connect(self._parent.settings_tree_button_toggles)
        self.itemClicked.connect(self._parent.settings_tree_button_toggles)
        self.itemCollapsed.connect(self._parent.settings_tree_button_toggles)
        self.itemExpanded.connect(self._parent.settings_tree_button_toggles)

    ## builds a table onto a tree widget item
    def build_tree_table_widget(self, label: QTreeWidgetItem, index_of_child, dict_pos):
        container = QTreeWidgetItem(label)
        container.setFirstColumnSpanned(True)
        container.setData(4, 0, dict_pos)
        # add parent tree item to root
        cursor = self._cursor
        logger = self.logger
        table = DelimitersTableView(self, logger, cursor, container, self.cliopt)
        self.tables.append(table)
        index_of_child += 1
        return index_of_child

    ## helper method to add children to container items
    def set_up_child(
        self,
        dict_key,
        parent,
        index_of_child,
        var_name,
        var_type,
        var_tooltip,
        var_initial_val,
        combobox=False,
        combobox_item_tooltips=[],
    ):
        column_label_list = ["", var_name, var_type, str(repr(var_initial_val))]
        child_container = QTreeWidgetItem(parent, column_label_list)
        _twi = child_container
        dict_pos = dict_key + "," + str(index_of_child) + "," + var_name
        _twi.setData(4, 0, dict_pos)
        _twi.setFlags(_twi.flags() | Qt.ItemIsEditable)
        if var_tooltip != "" and var_tooltip != None:
            for col in range(self.columnCount()):
                _twi.setToolTip(col, var_tooltip)
        if combobox == True:
            for col in range(self.columnCount()):
                _twi.setToolTip(col, combobox_item_tooltips[0])
            _cmb = QComboBox()
            _cmb.addItem("Disabled", False)
            _cmb.addItem("Enabled", True)

            if (
                combobox_item_tooltips
                and combobox_item_tooltips[0] != None
                and combobox_item_tooltips[0] != ""
            ):
                _cmb.setItemData(0, combobox_item_tooltips[0], Qt.ToolTipRole)
            if (
                combobox_item_tooltips
                and combobox_item_tooltips[1] != None
                and combobox_item_tooltips[1] != ""
            ):
                _cmb.setItemData(1, combobox_item_tooltips[1], Qt.ToolTipRole)
            _cmb.setObjectName(dict_pos)
            if var_initial_val == False:
                _cmb.setCurrentIndex(_cmb.findText("Disabled"))
            elif var_initial_val == True:
                _cmb.setCurrentIndex(_cmb.findText("Enabled"))
            _cmb.setSizeAdjustPolicy(QComboBox.AdjustToMinimumContentsLengthWithIcon)
            # _cmb.currentIndexChanged.connect(self.settings_tree_combo_box_index_changed)
            _cmb.currentTextChanged.connect(self.settings_tree_combo_box_index_changed)
            self.setItemWidget(
                _twi,
                3,
                _cmb,
            )
        index_of_child += 1
        return index_of_child

    ## updates the type field to reflect the value
    def update_settings_tree_type_field_text(self, item):
        object_string = str(item.data(4, 0))
        object_list = object_string.strip("\n").split(",")
        sub_dict = self.cliopt["config"]["tree"]["items"][object_list[0]][
            int(object_list[1])
        ]["fields"]
        number_field = int(sub_dict["3"])
        if number_field <= 255:
            type_field = "uint8_t"
            item.setToolTip(2, "")
        elif number_field > 255 and number_field <= 65535:
            type_field = "uint16_t*"
            item.setToolTip(2, "The compiler will warn you about this type change")
        elif number_field > 65535:
            type_field = "uint32_t*"
            item.setToolTip(2, "The compiler will warn you about this type change")
        item.setText(2, type_field)

    ## called on combobox change
    def settings_tree_combo_box_index_changed(self, index):
        self.prompt_to_save = True
        self.windowtitle_set = False
        object_string = self.sender().objectName()
        object_list = object_string.strip("\n").split(",")
        object_list[1] = int(object_list[1])

        if object_list[0] in displayModels._settings_tree_display["config"]:
            _tt = displayModels._settings_tree_display["config"][object_list[0]][
                object_list[2]
            ]["tooltip"]
        else:
            _tt = displayModels._settings_tree_display[object_list[0]][object_list[2]][
                "tooltip"
            ]
        if object_list[0] == "builtin methods":

            _twi = self.currentItem()
            combobox = self.itemWidget(_twi, 3)

            if combobox.currentText() == "Enabled":
                self.cliopt[object_list[0]]["var"][object_list[2]] = True
                SettingsTreeMethods.logger.info(
                    object_list[0] + " " + object_list[2] + " enabled"
                )
                for col in range(self.columnCount()):
                    _twi.setToolTip(col, _tt[1])
            else:
                self.cliopt[object_list[0]]["var"][object_list[2]] = False
                SettingsTreeMethods.logger.info(
                    object_list[0] + " " + object_list[2] + " disabled"
                )
                for col in range(self.columnCount()):
                    _twi.setToolTip(col, _tt[0])

            self.update_code("setup.h", object_list[2], True)
            if object_list[2] == "outputToStream":
                self.update_code("setup.cpp", object_list[2], True)

            if (
                object_list[2] == "defaultFunction"
                or object_list[2] == "listCommands"
                or object_list[2] == "listSettings"
            ):
                if object_list[2] == "defaultFunction":
                    if combobox.currentText() == "Enabled":
                        self.cliopt["builtin methods"]["var"]["defaultFunction"] = True
                    elif combobox.currentText() == "Disabled":
                        self.cliopt["builtin methods"]["var"]["defaultFunction"] = False

                elif (
                    object_list[2] == "listCommands" or object_list[2] == "listSettings"
                ):
                    if (
                        combobox.currentText() == "Enabled"
                        and object_list[2] == "listCommands"
                    ):
                        list_commands = OrderedDict()
                        list_commands = {
                            str(self.cliopt["commands"]["primary id key"]): dict(
                                zip(
                                    dataModels.command_parameters_dict_keys_list,
                                    dataModels.LCcmdParam,
                                )
                            )
                        }
                        self.cliopt["commands"]["parameters"].update(list_commands)

                        self.command_tree.add_command_to_tree(                         
                            self.command_tree.invisibleRootItem(),
                        )
                    else:
                        self.command_tree.remove_command_from_tree("listCommands")

                    if (
                        combobox.currentText() == "Enabled"
                        and object_list[2] == "listSettings"
                    ):
                        list_settings = OrderedDict()
                        list_settings = {
                            str(self.cliopt["commands"]["primary id key"]): dict(
                                zip(
                                    dataModels.command_parameters_dict_keys_list,
                                    dataModels.LScmdParam,
                                )
                            )
                        }
                        self.cliopt["commands"]["parameters"].update(list_settings)

                        self.command_tree.add_command_to_tree(
                            self.command_tree.invisibleRootItem(),
                        )
                    else:
                        self.command_tree.remove_command_from_tree("listSettings")

            self.update_code("functions.h", object_list[2], True)
            self.update_code("functions.cpp", object_list[2], True)
            self.update_code("parameters.h", object_list[2], True)
            self.update_code("setup.cpp", object_list[2], True)

        if object_list[0] != "builtin methods":
            _twi = self.currentItem()
            combobox = self.itemWidget(_twi, 3)
            object_data = self.get_object_data(_twi)
            info = self.cliopt["config"]["var"][object_data["pos"][2]]

            if combobox.currentText() == "Enabled":
                info["value"] = True
                self.log_settings_tree_edit(_twi)
                for col in range(self.columnCount()):
                    _twi.setToolTip(col, _tt[1])
            elif combobox.currentText() == "Disabled":
                info["value"] = False
                self.log_settings_tree_edit(_twi)
                for col in range(self.columnCount()):
                    _twi.setToolTip(col, _tt[0])
            self.update_code("config.h", object_data["pos"]["2"], True)

    ## this is called after determining if an item is editable
    def edit_settings_tree_item(self, item):
        widget_present = self.itemWidget(item, 0)
        if widget_present != None:
            # self.edit_table_widget_item(widget_present)
            widget_present.edit(widget_present.currentIndex())
            return
        self.log_settings_tree_edit(item)
        self.editItem(item, 3)

    ## called when a user "activates" a tree item (by pressing enter)
    def settings_tree_item_activated(self, item):
        # expand/collapse QTreeWidgetItem that has children, if it has them
        if item.childCount() > 0:
            if item.isExpanded():
                item.setExpanded(False)
            else:
                item.setExpanded(True)
            return
        object_list = str(item.data(4, 0)).split(",")
        SettingsTreeMethods.logger.info(object_list[2] + " selected")
        self.edit_settings_tree_item(item)

    ## if the user double clicks on something, see if it is editable
    def check_if_settings_tree_col_editable(self, item, column):
        # allow the third column to be editable with mouse clicks
        if column == 3:
            self.edit_settings_tree_item(item)

    def log_settings_tree_edit(self, item, object_data=None):
        if object_data == None:
            object_data = self.get_object_data(item)
        info = self.cliopt["config"]["var"][object_data["pos"][2]]
        val_type = object_data["type"]
        val = object_data["value"]
        if self.loading:
            SettingsTreeMethods.logger.info(
                "set "
                + object_data["pos"][2]
                + " to "
                + "'"
                + str(val)
                + "' "
                + str(val_type)
            )
        else:
            SettingsTreeMethods.logger.info(
                "User set "
                + object_data["pos"][2]
                + " to "
                + "'"
                + str(val)
                + "' "
                + str(val_type)
            )
        SettingsTreeMethods.logger.debug(
            str("self.cliOpt['config']['var']['{}']:".format(object_data["pos"][2]))
            + "\n"
            + str(
                json.dumps(info, indent=2, sort_keys=False, default=lambda o: "object")
            )
        )

    def get_object_data(self, item):
        retval = {"type": "", "value": "", "pos": []}
        object_data_pos_string = str(item.data(4, 0))
        object_data_pos_list = object_data_pos_string.strip("\n").split(",")
        if len(object_data_pos_list) < 2:
            return -1
        else:
            retval["type"] = str(item.data(2, 0))
            retval["value"] = str(item.data(3, 0))
            retval["pos"] = object_data_pos_list
            return retval

    ## this is called any time an item changes; any time any column edits take place on settings tree, user or otherwise
    def settings_tree_edit_complete(self, item, col):
        self.prompt_to_save = True
        self.windowtitle_set = False
        if col != 3:
            return
        object_data = self.get_object_data(item)

        val = object_data["value"]
        if "'" in val:
            return  # already repr

        if object_data["pos"][0] == "builtin methods":
            return
        object_data["pos"][1] = int(str(object_data["pos"][1]))

        # process output
        if object_data["pos"][0] == "process output":
            item.setText(3, str(repr(val)))
            self.cliopt["process output"]["var"][object_data["pos"][2]] = val
            self.log_settings_tree_edit(item, object_data)
            self.update_code("setup.h", object_data["pos"][2], True)
            if object_data["pos"][2] == "outputToStream":
                self.update_code("setup.cpp", object_data["pos"][2], True)
            if object_data["pos"][2] == "defaultFunction":
                self.update_code("functions.h", object_data["pos"][2], True)
                self.update_code("functions.cpp", object_data["pos"][2], True)
            return

        # process parameters (setup.h)
        if object_data["pos"][0] == "process parameters":
            item.setText(3, "'" + str(val) + "'")
            self.log_settings_tree_edit(item, object_data)
            self.cliopt["process parameters"]["var"][item.text(1)] = val
            self.update_code("setup.h", item.text(1), True)
            return

        # config.h
        info = self.cliopt["config"]["var"][object_data["pos"][2]]
        tmp = ""
        if val == "enabled":
            tmp = True
        elif val == "disabled":
            tmp = False
        else:
            if val == "":
                tmp = 0
                item.setText(3, "'" + str(repr(tmp)) + "'")
            else:
                tmp = int(val)
                item.setText(3, "'" + str(repr(tmp)) + "'")
        if tmp == info["value"]:
            return
        # update the config dict
        info["value"] = tmp
        self.update_settings_tree_type_field_text(item)
        self.update_code("config.h", object_data["pos"][2], True)
        self.log_settings_tree_edit(item, object_data)

    ## this is called after determining if an item is editable
    def edit_item(self, item):
        widget_present = self.itemWidget(item, 0)
        if widget_present != None:
            # self.edit_table_widget_item(widget_present)
            widget_present.edit(widget_present.currentIndex())
            return
        self.log_settings_tree_edit(item)
        self.editItem(item, 3)


# settings_tree methods
class SettingsTreeMethods(object):
    ## the constructor
    def __init__(self):
        super(SettingsTreeMethods, self).__init__()
        SettingsTreeMethods.logger = self.get_child_logger(__name__)
        SettingsTreeMethods._tree = displayModels._settings_tree_display
        tree_buttons = copy.deepcopy(dataModels.button_dict)
        tree_buttons["buttons"].update(
            {
                "edit": copy.deepcopy(dataModels.button_sub_dict),
                "clear": copy.deepcopy(dataModels.button_sub_dict),
                "default": copy.deepcopy(dataModels.button_sub_dict),
                "collapse": copy.deepcopy(dataModels.button_sub_dict),
            }
        )
        tree_buttons["buttons"]["edit"]["QPushButton"] = self.ui.edit_setting_button
        tree_buttons["buttons"]["clear"]["QPushButton"] = self.ui.clear_setting_button
        tree_buttons["buttons"]["default"][
            "QPushButton"
        ] = self.ui.default_setting_button
        tree_buttons["buttons"]["collapse"][
            "QPushButton"
        ] = self.ui.settings_tree_collapse_button
        tree_buttons["buttons"]["collapse"]["enabled"] = True
        self.settings_tree_buttons = tree_buttons

    def build_settings_tree(self):
        container = self.ui.settings_tree_container
        container.layout = QHBoxLayout(container)
        self.settings_tree = SettingsTreeWidget(
            self, self.cliOpt, self.session, SettingsTreeMethods.logger
        )
        container.layout.addWidget(self.settings_tree)
        container.setLayout(container.layout)
        return self.settings_tree


# end of file
