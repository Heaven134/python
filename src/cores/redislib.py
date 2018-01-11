
#!/usr/bin/python
#coding=utf-8

import os

WORK_NODE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# print CURRENT_DIR
os.sys.path.insert(0, os.path.dirname(WORK_NODE_DIR))


from src.cores import my_logger as logging

import sys
import redis
from src.conf import config


class RedisTools(object):


    def __init__(self):
	try:
		redisconfig = config['redisconf']
	        self.pool    = redis.ConnectionPool(host=redisconfig['host'], port=redisconfig['port'], db=0)
        	self.Redis   = redis.Redis(connection_pool = self.pool)
	except Exception, e:
        	logging.error('conn redis error,the error info is %s',e)
	        sys.exit(1)
    # push a new link at the end of list
    def pushLink(self,key,value):
        return self.Redis.lpush(key,value)

    #return the last link
    def lpopLink(self,rlist,value):
        return self.Redis.lpop(rlist)

    #return the first link
    def rpopLink(self,rlist,value):
        return self.Redis.rpop(rlist)

    #get length of list
    def lenList(self,rlist):
        return self.Redis.llen(rlist)

    #init list 
    def delList(self,rlist):
        return self.Redis.delete(rlist)

    def set(self,key,value):
	return self.Redis.set(key,value)
 
    def hset(self, name, key, value):
	return self.Redis.hset(name, key, value)

    def hget(self, name, key):
        return self.Redis.hget(name, key)

    def getPipeLine(self):
	return self.Redis.pipeline(transaction=False)
	#return self.Redis.pipeline()

    def lindex(self, name, index):
	return self.Redis.lindex(name,index)
