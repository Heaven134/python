#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright 2014-2020 by Baidu. All Rights Reserved.
# gengmzh
# 2014-10-22

import os, sys, logging, logging.config

# logging
CORES_DIR = os.path.dirname(__file__)
WORK_TASK_DIR = os.path.dirname(CORES_DIR)

class CuteLogger(logging.Logger):

    def __init__(self, name, level=logging.NOTSET):
        super(CuteLogger, self).__init__(name, level)
        #base files
        self.base_files = []

    def set_base_files(self, base_files = ()):
        '''
        base_files: 父类中封装了打印日志方法，子类调用时需要剔除该调用栈针以输出子类的文件名、方法和代码行号
        '''
        if base_files:
            for _f in base_files:
                if _f[-4:].lower() in ['.pyc', '.pyo']:
                    _f = _f[:-4] + '.py'
                self.base_files.append(os.path.normcase(_f))

    def findCaller(self):
        """
        Find the stack frame of the caller so that we can note the source
        file name, line number and function name.
        """
        f = logging.currentframe()
        #On some versions of IronPython, currentframe() returns None if
        #IronPython isn't run with -X:Frames.
        if f is not None:
            f = f.f_back
        rv = "(unknown file)", 0, "(unknown function)"
        while hasattr(f, "f_code"):
            co = f.f_code
            filename = os.path.normcase(co.co_filename)
            if filename == logging._srcfile:
                f = f.f_back
                continue
            elif filename in self.base_files and f.f_back is not None:
                f = f.f_back
                continue
            rv = (co.co_filename, f.f_lineno, co.co_name)
            break
        return rv

logging.setLoggerClass(CuteLogger)
logging.config.fileConfig(os.path.join(WORK_TASK_DIR, 'conf', 'logging.conf'))
my_logger = logging.getLogger("main")
logging.setLoggerClass(logging.Logger)



