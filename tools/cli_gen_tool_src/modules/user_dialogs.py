import os
from PySide6.QtWidgets import QDialog, QFileDialog, QDialogButtonBox, QStyle
from PySide6.QtCore import Qt, QFile, QDir, QRegularExpression


class UserDialogs(object):
    def __init__(self) -> None:
        super(UserDialogs, self).__init__(__name__)
        UserDialogs.logger = self.get_child_logger(__name__)

    # TODO fix icon
    def create_file_error_qdialog(self, error_type: str, qfile: QFile):
        """creates an error dialog

        Args:
            error_type (str): error description
            qfile (QFile): file information
        """
        UserDialogs.logger.warning(error_type + " " + qfile.fileName() + " error.")
        self.create_qdialog(
            error_type,
            Qt.AlignCenter,
            0,
            error_type + " " + qfile.fileName() + " error.",
            None,
            None,
            self.ui.messageBoxCriticalIcon,
        )

    def get_project_dir(self) -> str:
        """get valid os path to project

        Returns:
            str: valid os path or None
        """
        open_on_dir = ""
        output_dir = self.session["opt"]["cli_output_dir"]
        if output_dir == None:
            output_dir = self._parent.lib_root_path
        if os.path.exists(output_dir):
            open_on_dir = output_dir
        else:
            open_on_dir = QDir.homePath()
        dir_dlg = QFileDialog(self)
        _dlg_result = dir_dlg.getExistingDirectory(
            self,
            "Select output directory",
            open_on_dir,
            options=QFileDialog.DontUseNativeDialog
            | QFileDialog.ShowDirsOnly
            | QFileDialog.DontResolveSymlinks,
        )
        if _dlg_result == QFileDialog.Rejected:
            b = QDialogButtonBox.StandardButton
            buttons = [b.Ok, b.Close]
            button_text = ["Select output directory", "Cancel"]
            result = self.create_qdialog(
                self._parent,
                "You must select an output directory to generate files.",
                Qt.AlignCenter,
                Qt.NoTextInteraction,
                "Error, no output directory selected!",
                buttons,
                button_text,
                QStyle.StandardPixmap.SP_MessageBoxCritical,
                self._parent.qscreen,
            )
            if result == 3:
                return None

        _dir = QDir(_dlg_result)
        _result = _dir.toNativeSeparators(_dir.absolutePath())
        if os.path.exists(_result):
            UserDialogs.logger.info("valid directory selected:\n" + str(_result))
            return _result
        else:
            UserDialogs.logger.info("invalid directory selected")
            return None

    def open_file(self, checked: bool = False, path: str = "") -> int:
        """opens a cli options file and does simple validity check

        Args:
            checked (bool, optional): action checked bool. Defaults to False.
            path (str, optional): absolute file path. Defaults to "".

        Returns:
            int: size if greater than zero, error code if zero or less.
        """
        if not os.path.exists(path):
            UserDialogs.logger.info("open CLI settings file dialog")
            # inherit from parent QMainWindow (block main window interaction while dialog box is open)
            dlg = QFileDialog(self)
            dlg.setFileMode(QFileDialog.ExistingFile)
            dlg.setNameFilter("Settings json (*.json)")
            dlg.setViewMode(QFileDialog.Detail)
            fileName = dlg.getOpenFileName(options=QFileDialog.DontUseNativeDialog)
            if dlg.Accepted:
                path = fileName[0]
            else:
                UserDialogs.logger.info("dialog cancelled")
                return 0  # dialog cancelled

        if path == "" or not os.path.exists(path):
            UserDialogs.logger.info("CLI settings file path error")
            return -1  # path error

        file = QFile(path)
        read_json_result = self.read_json(file)

        if read_json_result[0] >= 0 and read_json_result[1]["type"] == "cli options":
            if self._parent.prompt_to_save == True:
                regexp = QRegularExpression("[^\/]*$")
                match = regexp.match(path)
                if match.hasMatch():
                    filename = str(match.captured(0))
                b = QDialogButtonBox.StandardButton
                buttons = [b.Ok, b.Close]
                button_text = ["Save", "Cancel"]
                result = self.create_qdialog(
                    self._parent,
                    "Do you want to save your current work?",
                    Qt.AlignCenter,
                    Qt.NoTextInteraction,
                    f"Save before opening {filename}",
                    buttons,
                    button_text,
                    QStyle.StandardPixmap.SP_MessageBoxCritical,
                    self._parent.qscreen,
                )
                if result == QDialog.Accepted:
                    self.save_file()
            self.cliOpt = read_json_result[1]
        else:
            UserDialogs.logger.info("Incorrect json type")
            self.create_file_error_qdialog("Incorrect json type", file)
            return -2  # incorrect json type

        # empty the trees
        UserDialogs.logger.debug("clearing trees")
        self.settings_tree.clear()
        self.command_tree.clear()

        # rebuild the trees from the new cli options file
        UserDialogs.logger.debug("rebuilding trees")
        self.cliOpt["commands"]["primary id key"] = "0"
        self.session["opt"]["save_file_path"] = path
        self._parent.loading = True
        self.rebuild_command_tree()
        self.rebuild_settings_tree()
        self._parent.loading = False
        self.display_initial_code_preview()
        self.prompt_to_save = False
        self.windowtitle_set = False
        self.set_main_window_title()

        # move `path` to index 0
        UserDialogs.logger.debug(
            f"move this path to front of recent files list:\n{path}"
        )
        paths = self.session["opt"]["recent_files"]["paths"]
        if path in paths and paths.index(path) != 0:
            paths.insert(0, paths.pop(paths.index(path)))

        # remake menu
        UserDialogs.logger.debug("remake recent files menu")
        self.ui.actionOpen_Recent.setMenu(self.get_recent_files_menu())
        return read_json_result  # return size of file read
