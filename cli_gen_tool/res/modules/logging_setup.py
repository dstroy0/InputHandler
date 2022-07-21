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

from __future__ import absolute_import
import logging
from res.modules.dev_qol_var import log_file_handler, _log_formatter


class QPlainTextEditLogger(logging.Handler):
    def __init__(self, parent):
        super(QPlainTextEditLogger, self).__init__()
        self.widget = parent.log.dlg.logHistoryPlainTextEdit
        # settings for the widget are in the `logHistoryDialog.ui` file

    def emit(self, record):
        self.widget.appendPlainText(_log_formatter.format(record))


class Logger(object):
    def __init__(self):
        super().__init__()

    def setup_file_handler():
        log_file_handler.setLevel(logging.INFO)
        log_file_handler.setFormatter(_log_formatter)

    def get_file_handler():
        return log_file_handler

    def get_stream_handler():
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.INFO)
        stream_handler.setFormatter(_log_formatter)
        return stream_handler

    def get_logger(self, name):

        log_handler = QPlainTextEditLogger(self)

        logger = logging.getLogger(name)
        logger.setLevel(logging.INFO)
        logger.addHandler(Logger.get_file_handler())
        logger.addHandler(Logger.get_stream_handler())
        logger.addHandler(log_handler)
        return logger
