#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

WORK_NODE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# print CURRENT_DIR
os.sys.path.insert(0, os.path.dirname(WORK_NODE_DIR))

from src.cores import my_logger as logger


logger.info('----------init -----')
