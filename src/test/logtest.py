#!/usr/bin/env python
#coding=utf8

#导入包
import logging   
#基础设置
logging.basicConfig(filename = 'test.log',level = logging.INFO, format = '[%(asctime)s %(levelname)s] %(message)s', datefmt = '%Y-%m-%d %H:%M:%S')
#写日志，以不同的级别。
logging.debug('debug log')
logging.info('info log')
logging.warning('warning log')
logging.error('error log')
logging.critical('critial log')
