##
# @file logging_setup.py
# @author Douglas Quigg (dstroy0 dquigg123@gmail.com)
# @brief MainWindow external methods
# @version 1.0
# @date 2022-07-19
# @copyright Copyright (c) 2022
# Copyright (C) 2022 Douglas Quigg (dstroy0) <dquigg123@gmail.com>
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# version 3 as published by the Free Software Foundation.

# imports
from __future__ import absolute_import
import os
import logging
from logging.handlers import RotatingFileHandler
from PySide6.QtCore import QDir


## this class displays the session log history
class QPlainTextEditLogger(logging.Handler):
    def __init__(self, parent):
        super(QPlainTextEditLogger, self).__init__()
        self.widget = parent.log.dlg.logHistoryPlainTextEdit
        self.parent = parent
        # settings for the widget are in the `logHistoryDialog.ui` file

    def emit(self, record):
        self.widget.appendPlainText(Logger._log_formatter.format(record))


## logging api
class Logger(object):
    level_lookup = {
        10: "DEBUG",
        20: "INFO",
        30: "WARNING",
        40: "ERROR",
        50: "CRITICAL",
    }
    file_log_level = logging.DEBUG  # file log level
    stream_log_level = logging.INFO  # terminal log level
    session_history_log_level = (
        logging.INFO
    )  # session history widget log level (bound to F1)
    root_log_level = logging.INFO

    # log filesize
    # kb = 2^10 == 1024 bytes
    _KB = 2**10
    # mb = 2^2^10 == 1048576 bytes
    _MB = 2**2**10
    _log_path = "/tools/logs/"
    _log_filename = "cli_gen_tool.log"
    _log_format = "%(asctime)s - [%(levelname)s] -  %(name)s - (%(filename)s).%(funcName)s(line:%(lineno)d) - %(message)s"
    _log_formatter = logging.Formatter(_log_format)

    # log filehandler
    file_log_handler = ""

    # stream handler
    stream_log_handler = ""

    # session handler
    session_log_handler = ""

    # root
    root_log_handler = ""

    ## the constructor
    def __init__(self):
        super(Logger, self).__init__()

    ## This is called to set up the log file handler in MainWindow.__init__()
    def setup_file_handler(lib_root_path):
        # logfile pathing
        _path = QDir(lib_root_path + Logger._log_path)
        _abs_native_path = _path.toNativeSeparators(_path.absolutePath())
        if not os.path.isdir(_abs_native_path):
            os.mkdir(_abs_native_path)
        # log filehandler
        Logger.file_log_handler = RotatingFileHandler(
            _abs_native_path + _path.separator() + Logger._log_filename,
            "a",
            10 * Logger._MB,
            backupCount=5,
        )
        Logger.file_log_handler.setLevel(Logger.file_log_level)
        Logger.file_log_handler.setFormatter(Logger._log_formatter)

    ## external modules are children of MainWindow's logging instance
    def get_child_logger(parent, name):
        return parent.getChild(name)

    ## returns the log_file_handler
    def get_file_handler():
        return Logger.file_log_handler

    ## returns the stream_handler
    def get_stream_handler():
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(Logger.stream_log_level)
        stream_handler.setFormatter(Logger._log_formatter)
        Logger.stream_log_handler = stream_handler
        return stream_handler

    ## initializes the logger; returns the root logger
    def initialize_logger(self, name):
        logger = logging.getLogger(name)
        logger.setLevel(Logger.session_history_log_level)
        logger.addHandler(Logger.get_stream_handler())
        Logger.root_log_handler = logger
        return logger

    ## sets up window log history
    def set_up_window_history_logger(self):
        log_handler = QPlainTextEditLogger(self)
        Logger.session_log_handler = log_handler
        Logger.root_log_handler.addHandler(log_handler)


# end of file
