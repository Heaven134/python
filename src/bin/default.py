# /usr/env python
# -*- coding: UTF-8 -*-


import os    

WORK_NODE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# print CURRENT_DIR
os.sys.path.insert(0, os.path.dirname(WORK_NODE_DIR))

import random
import MySQLdb
from src.cores import dbutils
from src.cores import dblib
from src.cores import redislib
import math
import redis
import re
import httplib
import json
import time
from src.cores import HttpUtils
from src.conf import config
from src.cores import my_logger as logging


#设置日志信息
def setLogInfo():
        # 配置日志信息  
        logging.basicConfig(level=logging.DEBUG,
                            format='[%(asctime)s %(levelname)s] %(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S',
                            filename='heyinliang-hot.log')
        # 定义一个Handler打印INFO及以上级别的日志到sys.stderr  
        console = logging.StreamHandler()
        console.setLevel(logging.DEBUG)
        # 设置日志打印格式  
        formatter = logging.Formatter('[%(asctime)s %(levelname)s] %(message)s')
        console.setFormatter(formatter)
        # 将定义好的console日志handler添加到root logger  
        logging.getLogger('').addHandler(console)




if __name__ == '__main__':

	#setLogInfo()

        db = dbutils.dbutils()
	#now = time.time()
        #activityids = []
        #acttime = db.getActivityTime()
        #for r in acttime:
        #        actid = r['activity_id']
        #        if now < r['start_time']:
        #                logging.info('the activity (id:%s) has not start  ',actid)
        #        elif now > r['end_time']:
        #                logging.info('the activity (id:%s) is end ',actid)
        #        else:
        #                activityids.append(actid)

	
	redis = redislib.RedisTools()
	pipe = redis.getPipeLine()
	songinfos = db.getDefaultSongInfos()
	for actid,songinfo in songinfos.items():
	    #if actid in activityids:
		logging.info('---actid %s  song %s--',actid,songinfo)
		pipe.hset('default_'+str(actid),'count',1000)
		pipe.hset('default_'+str(actid),'size',len(songinfo))
		for num in range(1,1001):
			logging.info('begin to push %s to redis',num)
			random.shuffle(songinfo)
			pipe.delete('default_'+str(actid)+'_'+str(num))
			for songid in songinfo:
				pipe.lpush('default_'+str(actid)+'_'+str(num),songid)
        pipe.execute()
	
			
 












