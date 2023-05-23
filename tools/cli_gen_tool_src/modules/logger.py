##
# @file logger.py
# @author Douglas Quigg (dstroy0 dquigg123@gmail.com)
# @brief logging methods
# @version 1.0
# @date 2023-05-22
# @copyright Copyright (c) 2023
# Copyright (C) 2023 Douglas Quigg (dstroy0) <dquigg123@gmail.com>
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# version 3 as published by the Free Software Foundation.

from __future__ import absolute_import
import os
import logging
from logging.handlers import RotatingFileHandler


## this class displays the session log history
class QPlainTextEditLogger(logging.Handler):
    """session log history

    Args:
        logging (logging.Handler): log message handler
    """

    def __init__(self, widget):
        """the constructor

        Args:
            widget (QWidget): parent widget
        """
        super().__init__()
        self.widget = widget
        # settings for the widget are in the `logHistoryDialog.ui` file

    def emit(self, record):
        """emits changes

        Args:
            record (str): log message
        """
        self.widget.appendPlainText(Logger.log_formatter.format(record))


## logging api
class Logger(object):
    """logging api

    Args:
        object (object): base object specialization
    """

    level_lookup = {
        10: "DEBUG",
        20: "INFO",
        30: "WARNING",
        40: "ERROR",
        50: "CRITICAL",
    }
    session_log_level = logging.INFO  # global log level

    # log filesize
    # kb = 2^10 == 1024 bytes
    kb = 2**10
    # mb = 2^2^10 == 1048576 bytes
    mb = 2**2**10

    ## log filename
    log_filename = "cli_gen_tool.log"

    ## log format
    log_format = "%(asctime)s - [%(levelname)s] - (%(filename)s).%(funcName)s(line:%(lineno)d) - %(message)s"

    ## global formatter
    log_formatter = logging.Formatter(log_format)

    ## logging handlers
    root_log_handler = None
    stream_log_handler = None
    file_log_handler = None
    session_log_handler = None

    ## the constructor
    def __init__(self) -> None:
        super(Logger, self).__init__()

    def setup_logging(self, name):
        root_log_handler = logging.getLogger(name)
        root_log_handler.setLevel(Logger.session_log_level)
        root_log_handler.info("logging service initialized")
        Logger.root_log_handler = root_log_handler
        stream_log_handler = logging.StreamHandler()
        stream_log_handler.setLevel(Logger.session_log_level)
        stream_log_handler.setFormatter(Logger.log_formatter)
        Logger.stream_log_handler = stream_log_handler
        Logger.root_log_handler.addHandler(stream_log_handler)

    ## returns a logging object if setup_logging() has been called; else None
    def get_root_logger(self):
        return Logger.root_log_handler

    ## returns a logging object if setup_logging() has been called; else None
    def get_stream_logger(self):
        return Logger.stream_log_handler

    ## returns a logging object if setup_logging() and setup_file_handler() have been called and completed successfully; else None
    def get_file_handler(self):
        return Logger.file_log_handler

    ## This is called to set up the log file handler in MainWindow.__init__()
    def setup_file_handler(self):
        """sets up log file handler, requires Pathing.set_pathing()"""
        # logfile pathing
        if not os.path.isdir(self.logs_path):
            return -1
        # log filehandler
        file_log_handler = RotatingFileHandler(
            self.logs_path + os.path.sep + Logger.log_filename,
            "a",
            10 * Logger.mb,
            backupCount=5,
        )
        file_log_handler.setLevel(Logger.session_log_level)
        file_log_handler.setFormatter(Logger.log_formatter)
        Logger.root_log_handler.info(
            "Log file path: " + self.logs_path + os.path.sep + Logger.log_filename
        )
        Logger.file_log_handler = file_log_handler
        return file_log_handler

    ## each module that logs gets a child logger from the root logger
    def get_child_logger(self, name):
        return Logger.root_log_handler.getChild(name)

    ## sets up window log history
    def set_up_window_history_logger(self, widget):
        """sets up session log history app window

        Args:
            widget (QWidget): session log history container
        """
        Logger.session_log_handler = QPlainTextEditLogger(widget)
        Logger.root_log_handler.addHandler(Logger.session_log_handler)

    ## sets handler log levels
    def set_log_levels(self):
        """sets log levels"""
        self.parent_instance.root_log_handler.setLevel(Logger.session_log_level)
        self.parent_instance.file_log_handler.setLevel(Logger.session_log_level)
        self.parent_instance.stream_log_handler.setLevel(Logger.session_log_level)
        self.parent_instance.session_log_handler.setLevel(Logger.session_log_level)


# end of file
