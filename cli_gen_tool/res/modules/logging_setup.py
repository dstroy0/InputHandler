##
# @file logging.py
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
import logging, datetime


class QPlainTextEditLogger(logging.Handler):
    def __init__(self, parent):
        super(QPlainTextEditLogger, self).__init__()
        self.widget = parent.log.dlg.logHistoryPlainTextEdit
        self.widget.setReadOnly(True)
        
    def emit(self, record):        
        log_formatter = logging.Formatter(Logger._log_format)
        msg = log_formatter.format(record)        
        self.widget.appendPlainText(msg)

class Logger(object):
    _log_filename = str(datetime.date.today()) + "-cli_gen_tool.log"
    _log_format = "%(asctime)s - [%(levelname)s] -  %(name)s - (%(filename)s).%(funcName)s(line:%(lineno)d) - %(message)s"
    
    def __init__(self):
        super().__init__()                    
    
    def get_file_handler():
        file_handler = logging.FileHandler(Logger._log_filename)
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(logging.Formatter(Logger._log_format))
        return file_handler

    def get_stream_handler():
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.INFO)
        stream_handler.setFormatter(logging.Formatter(Logger._log_format))
        return stream_handler
                    
    def get_logger(self,name):        
        
        log_handler = QPlainTextEditLogger(self)
        
        logger = logging.getLogger(name)
        logger.setLevel(logging.INFO)
        logger.addHandler(Logger.get_file_handler())
        logger.addHandler(Logger.get_stream_handler())                
        logger.addHandler(log_handler)
        return logger