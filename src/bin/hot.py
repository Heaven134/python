# /usr/env python
# -*- coding: UTF-8 -*-

import os    

WORK_NODE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# print CURRENT_DIR
os.sys.path.insert(0, os.path.dirname(WORK_NODE_DIR))

import random
import logging
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
from src.cores import my_logger as logging


def getVThumb(actid,vids):
	hu = HttpUtils.HttpUtils()
	logging.info('get V collect info ,the actid is  %s,the   vids %s ----',actid,vids)
	res = hu.getHttpReqByUser('collect',actid,vids)
	return res

offlinesong = {}
def getOfflineSong(db):
	global  offlinesong
	if len(offlinesong) == 0:
		offlinesong = db.getOfflineSong()
		logging.info('the offline song info is %s',offlinesong)
	return offlinesong



#大v的歌曲随机取5首歌
def getSongIDs(db,key,obj):
	logging.info('get V collect info ,the request result is %s',obj)
	actid = key.split("_")[1]
	offsongids = getOfflineSong(db)

	songids  = []
        d = eval(obj)
        
        if len(d['result']) > 0:
        	r = d['result']
		for i in r:
 			songids.append(long(i['itemid']))

	logging.info('get original  V thumb songs info ,the songids is [%s]',songids)

	#如果大V点赞的歌曲有下线的，将其删除
	logging.debug('check the V collect songinfo ,the actid is %s,contain actid %s',actid,offsongids.has_key(actid))
	if offsongids.has_key(actid) and len(offsongids[actid]) != 0:
		for songid in offsongids[actid]:
			if songid in songids:
				logging.info('the V collect song (songid:%s) is offline ,remove it from list ',songid)
				songids.remove(songid)
	random.shuffle(songids)
	return songids[:5]


if __name__ == '__main__':

	#用于存储热榜最后的结果，key是 topicid_actid,values 为songids	
	hotdict = {}

	db = dbutils.dbutils()
        res = db.getTopSong()
	if res != False:
	    for i in res:
		topicid = i['topic_id']
		actid = i['activity_id']
		songid = i['song_id']
		#logging.info('------actid :%s songid  :%s -------',actid,songid)
		if hotdict.has_key(str(topicid)+'_'+str(actid)):
			hotdict[str(topicid)+'_'+str(actid)].append(songid)
		else:	
			hotdict[str(topicid)+'_'+str(actid)] = [songid]

	logging.debug('get top200 songs ,the result is %s',hotdict)

        #获取20个大Vusrid
        vids = db.getVuserid()
        ids = ''
	if vids != False:
            for i in vids:
                uid = i['user_id']
                ids = ids + str(uid) + ','
        if len(ids) > 0:
                ids = ids[:len(ids)-1]
        logging.info('get V userid ,the info is %s,and the deal result is [%s]',vids,ids)



	for key,songids in  hotdict.items():
		random.shuffle(songids) #top200打散
		hotdict[key]=songids[:5] #然后取前五个
		logging.info('get 5 songs from top 200 ,the result is %s',hotdict)	
		v = getVThumb(key,ids)
		logging.debug('get V thumb info of the activity(actid :%s) ,the result is %s',key,v)
        	songidsV = getSongIDs(db,key,v)
		logging.info('get V thumb songinfos (actid:%s),the result is %s',key,songidsV)
		#logging.debug('----type(songids) %s----type(songidsV)  %s-------',songids,songidsV)
		hotdict[key].extend(songidsV)
		hotdict[key] = list(set(hotdict[key]))
	logging.info('select 5 songs from top200 and 5 from V thumb songs  ,the result (activityid:songids)is %s',hotdict)





	#如果大v收藏的歌曲不够五首歌，用编辑推荐的歌曲补齐五首，加上前面的五首歌，目前每个活动十首歌
	ss = db.getSuggestSong()	
	logging.info('get suggest songinfo ,the info is %s',ss)
	for key,songids in ss.items():
        	random.shuffle(songids)
		for songid in songids:
		    if hotdict.has_key(key) and len(hotdict[key]) < 10 and (songid not in hotdict[key] ):
			logging.info('the activity(actid:%s) not 10 songs , add the suggest songs (songid:%s) to the activity ',key,songid)
			hotdict[key].append(songid) 

	logging.info('add suggest song end ,the hot dict is %s',hotdict)

	#其他歌曲中随机选10首歌	
	logging.info('begin to add random songs to the result....')
	res = db.getNotTopSong()
	logging.debug('not top 200 data %s',res)
	for key,songids in res.items():
	    random.shuffle(songids)
	    for songid in songids:
	        if songid not in hotdict[key] and len(hotdict[key]) < 20:
			logging.info('add the not top 200 song(songid:%s) to the result',songid)
			hotdict[key].append(songid)

	logging.info('calc hot songinfo finish .the result is %s',hotdict)

	
	#将结果写入redis
	#now = time.time()
	#activityids = []
	#acttime = db.getActivityTime()	
	#for r in acttime:
	#	actid = r['activity_id']
	#	if now < r['start_time']:
	#		logging.info('the activity (id:%s) has not start  ',actid) 
	#	elif now > r['end_time']:
	#		logging.info('the activity (id:%s) is end ',actid)
	#	else:
	#		activityids.append(actid)
	#将正在进行的活动的信息写入redis
	redis = redislib.RedisTools()
	pipe = redis.getPipeLine()
	for key,songids in hotdict.items():
	        actid = key.split('_')[1]
		logging.info('push the result to redis ,the actid is  %s  ,and the songids is  %s',actid,songids)
		pipe.delete('hot_'+bytes(actid))
		for songid in songids:
			pipe.rpush('hot_'+bytes(actid),songid)
        pipe.execute()

	logging.info('calc hot songs finish ,the result is %s',hotdict)	

			
 












