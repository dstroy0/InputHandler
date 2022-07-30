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

from res.modules.logging_setup import Logger
from res.modules.dev_qol_var import filestring_db

# command_tree methods
class CommandTreeMethods(object):
    def __init__(self) -> None:
        super(CommandTreeMethods,self).__init__()
        CommandTreeMethods.logger = Logger.get_child_logger(self.logger, __name__)