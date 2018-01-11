# /usr/env python
# -*- coding: UTF-8 -*-

import os    

WORK_NODE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# print CURRENT_DIR
os.sys.path.insert(0, os.path.dirname(WORK_NODE_DIR))

import sys
import random
import MySQLdb
from src.cores import dbutils
import math
import redis
import re
import httplib
import json
import datetime
from src.cores import redislib
from src.cores import matchsong
from src.cores import HttpUtils
from src.conf import config
from decimal import *
from src.cores import my_logger as logging

#list = [20, 16, 10, 5];
#random.shuffle(list)
#print "Reshuffled list : ",  list
#
#random.shuffle(list)
#print "Reshuffled list : ",  list

def getSongids(songids):
	idlist = []
	a = json.loads(songids)	
	r = a['songids']
	sids = r.split(',')
	for sid in sids:
		idlist.append(sid)
	return idlist

if __name__ == '__main__':
	db = dbutils.dbutils()
	task = db.getTaskInfo()
        
	addDict = {}
	delDict = {}
	taskids = []
	
	if task != False:
	    for r in task:
		taskid = r['task_id']	
		actid = r['activity_id']
		tasktype = r['task_type']
		content = r['content']
		status = r['status']
	
		songids = getSongids(content)

		#logging.debug('---songids----%s--',songids)
		taskids.append(taskid)
		if tasktype == 0:			
			if addDict.has_key(actid):
				addDict[actid].extend(songids)
			else:
				addDict[actid] = songids
		elif tasktype == 1:
			if delDict.has_key(actid):
                                delDict[actid].extend(songids)
                        else:
                                delDict[actid] = songids
	
	logging.debug('---re calc default list ,the addDict is %s',addDict)
       	logging.debug('---re calc default list ,the delDict is %s',delDict) 
	redis = redislib.RedisTools()
        pipe = redis.getPipeLine()
	for actid,songids in addDict.items():
		songids = list(set(songids))
		size = redis.hget('default_'+str(actid),'size')
		logging.debug('the size is %s',size)
		index = random.randint(0,int(size))
		logging.debug('the random is %s ',index)
		for num in range(1,1001):
			#logging.info('begin to insert data to redis ,the key is %s','default_'+str(actid)+'_'+str(num))
			key = redis.lindex('default_'+str(actid)+'_'+str(num),index)
			#logging.debug('the refvalue of the redis (key:%s) is %s','default_'+str(actid)+'_'+str(num),key)
			for sid in songids:
				pipe.linsert('default_'+str(actid)+'_'+str(num),'before',key,sid)
				#logging.debug('begin to insert data %s to redis ,the key is %s',sid,'default_'+str(actid)+'_'+str(num))
			#logging.info('insert data to redis end ,the key is %s','default_'+str(actid)+'_'+str(num))


        for actid,songids in delDict.items():
		songids = list(set(songids))
                for num in range(1,1001):
                        #logging.info('begin to delete from  redis ,the key is %s','default_'+str(actid)+'_'+str(num))
                        for sid in songids:
                                pipe.lrem('default_'+str(actid)+'_'+str(num),sid,0)
                                #logging.debug('begin to delete %s from redis ,the key is %s',sid,'default_'+str(actid)+'_'+str(num))

	
	pipe.execute()	

	logging.info('begin to update the task status ,the taskid is %s',taskids)
	r = 1
	if len(taskids) > 0:
		for tid in taskids:
			i=db.updateTaskStatus(tid)
			r = r&i
		if r==1:
			logging.info('update task status success !')
		else:
			logging.error('upate task status failed !')
	else:
		logging.info('no task to update status ')

