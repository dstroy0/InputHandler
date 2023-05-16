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
        super(QPlainTextEditLogger, self).__init__()
        self.widget = widget
        # settings for the widget are in the `logHistoryDialog.ui` file

    def emit(self, record):
        """emits changes

        Args:
            record (str): log message
        """
        self.widget.appendPlainText(Logger._log_formatter.format(record))


## logging api
class Logger(object):
    """logging api

    Args:
        object (object): base object specialization
    """

    log_setup_complete = False
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
    _KB = 2**10
    # mb = 2^2^10 == 1048576 bytes
    _MB = 2**2**10
    ## log file path
    _log_path = "/logs/"
    ## log filename
    _log_filename = "cli_gen_tool.log"
    # %(name)s -
    ## log format
    _log_format = "%(asctime)s - [%(levelname)s] - (%(filename)s).%(funcName)s(line:%(lineno)d) - %(message)s"
    _log_formatter = logging.Formatter(_log_format)

    ## the constructor
    def __init__(self) -> None:
        super(Logger, self).__init__()
    
    def get_root_logger(self, name):
        root_log_handler = logging.getLogger(name)
        root_log_handler.setLevel(Logger.session_log_level)                            
        root_log_handler.info("logging service initialized")
        return root_log_handler

    def get_stream_logger(self, root_log_handler):
        stream_log_handler = logging.StreamHandler()
        stream_log_handler.setLevel(Logger.session_log_level)
        stream_log_handler.setFormatter(Logger._log_formatter)
        root_log_handler.addHandler(stream_log_handler)
        return stream_log_handler
            
    ## This is called to set up the log file handler in MainWindow.__init__()
    def setup_file_handler(self):
        """sets up log file handler"""
        # logfile pathing
        path = os.path.abspath(
            os.path.join(self.inputhandler_save_path, Logger._log_path)
        )

        if not os.path.isdir(path):
            os.mkdir(path)
        # log filehandler
        self.file_log_handler = RotatingFileHandler(
            path + os.path.sep + Logger._log_filename,
            "a",
            10 * Logger._MB,
            backupCount=5,
        )
        self.file_log_handler.setLevel(Logger.session_log_level)
        self.file_log_handler.setFormatter(Logger._log_formatter)
        self.root_log_handler.info(
            "Log file path: " + path + os.path.sep + Logger._log_filename
        )

    ## external modules are children of MainWindow's logging instance
    def get_child_logger(self, name):
        """gets child logger for __name__

        Args:
            name (__name__): child name

        Returns:
            logging.Handler: child of self.root_log_handler
        """
        return self.root_log_handler.getChild(name)

    ## returns the log_file_handler
    def get_file_handler(self):
        """gets the log file handler

        Returns:
            logging.Handler: self.file_log_handler
        """
        return self.file_log_handler

    ## sets up window log history
    def set_up_window_history_logger(self, widget):
        """sets up session log history app window

        Args:
            widget (QWidget): session log history container
        """
        self.session_log_handler = QPlainTextEditLogger(widget)
        self.root_log_handler.addHandler(self.session_log_handler)

    ## sets handler log levels
    def set_log_levels(self):
        """sets log levels"""
        self.parent_instance.root_log_handler.setLevel(Logger.session_log_level)
        self.parent_instance.file_log_handler.setLevel(Logger.session_log_level)
        self.parent_instance.stream_log_handler.setLevel(Logger.session_log_level)
        self.parent_instance.session_log_handler.setLevel(Logger.session_log_level)


# end of file
