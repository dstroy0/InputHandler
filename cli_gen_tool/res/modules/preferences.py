##
# @file preferences.py
# @author Douglas Quigg (dstroy0 dquigg123@gmail.com)
# @brief MainWindow external methods
# @version 1.0
# @date 2022-08-23
# @copyright Copyright (c) 2022
# Copyright (C) 2022 Douglas Quigg (dstroy0) <dquigg123@gmail.com>
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# version 3 as published by the Free Software Foundation.

from __future__ import absolute_import
from res.modules.logging_setup import Logger

class PreferencesMethods(object):
    def __init__(self) -> None:
        super(PreferencesMethods, self).__init__()
        PreferencesMethods.logger = Logger.get_child_logger(self.logger, __name__)
        
    