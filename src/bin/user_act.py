# /usr/env python
# -*- coding: UTF-8 -*-

import sys
import os    
import commands

WORK_NODE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# print CURRENT_DIR
os.sys.path.insert(0, os.path.dirname(WORK_NODE_DIR))

from src.cores import dbutils
from src.cores import my_logger as logging




if __name__ == '__main__':
        params = len(sys.argv)
        logging.info('the len of the params is %s',params)
        if params <= 1:
                logging.error('the py script params is error')
                sys.exit(0)
        
        db = dbutils.dbutils()
        actids = db.getAct()
        for id in actids:
                cmd = 'sh user_act.sh  '+ sys.argv[1] +' '+ str(id)
                logging.info('begin to exec cmd [%s]',cmd)
                status,output = commands.getstatusoutput(cmd)
                if status == 0 :
                        logging.info('the cmd [%s] exec finished,the result is [%s]',cmd,output)
                else:
                        logging.error('the cmd [%s] exec error,the status is %s,and the result is [%s]',cmd,status,output)



