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
import os
import logging
from logging.handlers import RotatingFileHandler


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
    file_log_level = logging.INFO  # file log level
    stream_log_level = logging.INFO  # terminal log level
    session_history_log_level = (
        logging.INFO
    )  # session history widget log level (bound to F1)

    # log filesize
    # kb = 2^10 == 1024 bytes
    _KB = 2**10
    # mb = 2^2^10 == 1048576 bytes
    _MB = 2**2**10
    _log_path = "/logs/"
    _log_filename = "cli_gen_tool.log"
    _log_format = "%(asctime)s - [%(levelname)s] -  %(name)s - (%(filename)s).%(funcName)s(line:%(lineno)d) - %(message)s"
    _log_formatter = logging.Formatter(_log_format)

    # log filehandler
    log_file_handler = ""

    ## the constructor
    def __init__(self):
        super(Logger, self).__init__()

    ## This is called to set up the log file handler in MainWindow.__init__()
    def setup_file_handler(lib_root_path):
        # logfile pathing
        if not os.path.isdir(lib_root_path + Logger._log_path):
            os.mkdir(lib_root_path + Logger._log_path)
        # log filehandler
        Logger.log_file_handler = RotatingFileHandler(
            lib_root_path + Logger._log_path + Logger._log_filename,
            "a",
            10 * Logger._MB,
            backupCount=5,
        )
        Logger.log_file_handler.setLevel(Logger.file_log_level)
        Logger.log_file_handler.setFormatter(Logger._log_formatter)

    ## external modules are children of MainWindow's logging instance
    def get_child_logger(parent, name):
        return parent.getChild(name)

    ## returns the log_file_handler
    def get_file_handler():
        return Logger.log_file_handler

    ## returns the stream_handler
    def get_stream_handler():
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(Logger.stream_log_level)
        stream_handler.setFormatter(Logger._log_formatter)
        return stream_handler

    ## returns the root logger
    def get_logger(self, name):
        log_handler = QPlainTextEditLogger(self)
        logger = logging.getLogger(name)
        logger.setLevel(Logger.session_history_log_level)
        logger.addHandler(Logger.get_file_handler())
        logger.addHandler(Logger.get_stream_handler())
        logger.addHandler(log_handler)
        return logger


# end of file
