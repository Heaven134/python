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


responseDict = {}
ratioDict = {}



def enum(**enums):
    return type('Enum', (object,), enums)


Acts = enum(THUMB=1, VOTE=2, LISTEN=3)


	



def getThumbInfo(activityid):
	obj = {
              'error_code': 22000,
              'result': [
                  {
                      activityid: [
                          {
                              'num': 10,
                              'itemid': 1
                          },
                          {
                              'num': 100,
                              'itemid': 2
                          }
                      ]
                  }
              ]
          }
	return obj


#获取一个活动的所有的投票的信息
def getVoteInfo(activityid):
        obj = {
              'error_code': 22000,
              'result': [
                  {
                      activityid: [
                          {
                              'num': 85,
                              'itemid': 1
                          },
                          {
                              'num': 20,
                              'itemid': 2
                          }
                      ]
                  }
              ]
          }
        return obj

#获取某一个活动最大的点赞数或者投票数
def getMaxScore(dict):
	max = 0
	if len(dict.values())>0:
		for v in dict.values():
			if v > max:
			    max = v	
			    logging.debug('the max is %s',max)
                        else:
			    continue
	logging.debug('end ,the max is %s',max)
	return max


def getRatio(db,actid,type):
	actid = str(actid)
	#logging.debug('--get ratio -%s-',actid)
	global  ratioDict
	if len(ratioDict) == 0:
	        ratioDict = db.selectRatio()
	#logging.debug('ratioDict-------------%s',ratioDict.has_key('111'))
	if  ratioDict.has_key(actid):
		res = ratioDict[actid]
		if type == Acts.THUMB:
			return res['fav_ratio']
		elif type == Acts.VOTE:
			return res['vote_ratio']
		elif type == Acts.LISTEN:
			return res['listen_ratio']
        else:
		return 0


def calcOrderNo(songinfos):
	i=0
	for song in songinfos:
	    i=i+1
	    song.order_no = i
	return songinfos	








#获取点赞信息
#def GetThumbInfo(url):
#	#print '----url--------',url
#	r = random.randint(10, 20)
#	obj = { 'error_code': 22000, 'result': [ { url: { 'num':  } } ] }
#	return obj
#    	#conn = httplib.HTTPConnection(url)
#	#conn.request('get', '/')
#	#res = conn.getresponse().read()
#	#conn.close()
#	#return res 
def GetVoteInfo(url):
	r = random.randint(10, 20)
	obj = { 'error_code': 22000, 'result': [ { url: { 'num': r } } ] }
        return obj
def parseHttpResult(str):
	#logging.debug('parse http res ,the info is %s',str)
	dict  = {}
	d = eval(str)
	
	if len(d['result']['detail']) > 0:
		r = d['result']['detail']
		for i in r:
		    dict[i['itemid']] = int(i['scores'])
	return dict


def calcScore(db,actid,maxnum,num,type,songid = 0):
	logging.debug('calcScore ,the actid is %s ,the maxnum is %s ,num is %s ',actid,maxnum,num)
	base = getRatio(db,actid,type)
	if base == 0:
		return 0

	res = 0
	if int(maxnum) == int(num):
		res = base
	elif int(maxnum) == 0 or int(num) == 0:
		res = 0
	else:
		r = math.log(float(num))/math.log(float(maxnum))*base
                res = '{:.2f}'.format(Decimal(r))  
	logging.info('begin to calc score,type is %s , base is %s ,the songid is %s ,the maxnum is %s,and the current num is %s,and the score is %s',type,base,songid,maxnum,num,res ) 
	return res		



def getActivityNum(db,activity_id):
	activity_id = int(activity_id)
	#logging.info('begin to get the max listen num of the activity (id:%s)',activity_id)
        activitynum =  db.getActivityNum()
        logging.info('the all activity listen is %s', activitynum)
	maxlistennum = 0
        if activitynum.has_key(activity_id):
		maxlistennum = activitynum[activity_id]
	logging.info('the all activity listen is %s, the current actid is %s, the max listen num is %s', activitynum,activity_id,maxlistennum)
        return maxlistennum	




#def updateSongScore(songid,score):
#	logging.info('update the song score ,the songid is %s,and the socre is %s ',songid,score)
#	db = dbutils.dbutils(dblib.Mysql(config['dbconf']))
#	db.updateSongScore(songid,score);
#设置日志信息
def setLogInfo():
	# 配置日志信息  
        logging.basicConfig(level=logging.DEBUG,  
                            format='[%(asctime)s %(levelname)s] %(message)s',  
                            datefmt='%Y-%m-%d %H:%M:%S',  
                            filename='heyinliang.log')
        # 定义一个Handler打印INFO及以上级别的日志到sys.stderr  
        console = logging.StreamHandler()  
        console.setLevel(logging.INFO)  
        # 设置日志打印格式  
        formatter = logging.Formatter('[%(asctime)s %(levelname)-8s] %(message)s')  
        console.setFormatter(formatter)  
        # 将定义好的console日志handler添加到root logger  
        logging.getLogger('').addHandler(console)   


def getProSongs(actsongs):
	dict ={}
        for k,v in actsongs.items():
            info = k.split(',')
	    topicid = info[0]
            actid = info[1]
            songid = info[2]
	    pro = v.promotion
	    #print '---------------',info  ,  v.promotion
	    if pro == 1 :
                if dict.has_key(actid): 
                        dict[actid].append(songid)
                else:
                        tmplist =[]
                        tmplist.append(songid)
                        dict[actid] = tmplist
	logging.info('get promotion info .the res is %s',dict)
        return dict

def getVirtualNum(songinfo,startsong,endsong):
	#songinfo.order_no = startsong.order_no + 1
	#if startsong.visible_rank_score  >  endsong.visible_rank_score + 0.01:

        #正常情况下，分数+0.01
        songinfo.visible_rank_score = startsong.visible_rank_score - 0.01
        songinfo.visible_vote_num = startsong.visible_vote_num 
        songinfo.visible_listen_num = startsong.visible_listen_num
        songinfo.visible_thumb_num = startsong.visible_thumb_num

	if startsong.visible_listen_score != 0:
		songinfo.visible_listen_score = startsong.visible_listen_score - 0.01
		songinfo.visible_collect_score = startsong.visible_collect_score
		songinfo.visible_vote_score = startsong.visible_vote_score
	elif startsong.visible_listen_score == 0 and startsong.visible_collect_score != 0:
                songinfo.visible_listen_score = startsong.visible_listen_score 
                songinfo.visible_collect_score = startsong.visible_collect_score - 0.01
                songinfo.visible_vote_score = startsong.visible_vote_score
	elif startsong.visible_collect_score == 0 and startsong.visible_vote_score != 0:
                songinfo.visible_listen_score = startsong.visible_listen_score 
                songinfo.visible_collect_score = startsong.visible_collect_score 
                songinfo.visible_vote_score = startsong.visible_vote_score - 0.01


	#else:
        #    if (startsong.visible_vote_num + 1) < endsong.visible_vote_num :
        #        songinfo.visible_rank_score = startsong.visible_rank_score 
        #        songinfo.visible_vote_num = startsong.visible_vote_num - 1
        #        songinfo.visible_listen_num = startsong.visible_listen_num
        #        songinfo.visible_thumb_num = startsong.visible_thumb_num



	#	#投票量相同的情况下，点赞数+1
        #        songinfo.visible_vote_num = startsong.visible_vote_num
        #        songinfo.visible_listen_num = startsong.visible_listen_num + 1
        #        songinfo.visible_thumb_num = startsong.visible_listen_num 
	#
	#elif  (startsong.visible_thumb_num +1 ) >=  endsong.visible_thumb_num and (startsong.visible_listen_num +1 ) < endsong.visible_listen_num:
        #        songinfo.visible_vote_num = startsong.visible_vote_num 
        #        songinfo.visible_listen_num = startsong.visible_listen_num 
        #        songinfo.visible_thumb_num = startsong.visible_listen_num + 1	
	return songinfo


def calcVirtualScore(startindex,endindex,songlist,promotionSids):
	
	
	startSong = songlist[startindex]
	endSong = songlist[endindex]
	for index,songinfo in enumerate(songlist):
		for songid in promotionSids:
			if songinfo.songid == songid:
				songinfo = getVirtualNum(songinfo,startSong,endSong)
				startSong = songinfo
				songlist[index] = songinfo				
	return songlist
				
def calcVirOrderNo(songinfoarray,songinfos,limitNum,proNum,prosongids):
	
	if len(songinfoarray) < limitNum:
		return songinfoarray
	
	#for s in songinfos.values():
	#     if s.songid == 10165:
	#	logging.debug('the ori songinfo array is %s',s)
	newOrderNo = []

	hasPromotion = {}
	startIndex = limitNum-proNum + 1
	
	logging.info('the limitNum is %s,the pronum is %s,the promotion songids is %s',limitNum,proNum,prosongids)
	prosongidsbak = []
	for p in prosongids:
	    logging.info('the promotion song (%s) info is %s',p,songinfos[p])
	    if songinfos[p].order_no <= limitNum:
		hasPromotion[songinfos[p].songid] = songinfos[p].order_no
		#如果该歌曲的排名已经晋级，将不再处理,将其从待晋级的歌曲列表中移除
		if songinfos[p].order_no < (limitNum-proNum + 1):
			startIndex = startIndex + 1
			logging.info('the song[songid:%s,real orderno:%s] has promotioned ,remove id from promotion list',songinfos[p],songinfos[p].order_no)
	        elif songinfos[p].order_no >= (limitNum-proNum + 1):
			prosongidsbak.append(p)
                	startIndex = startIndex - 1
	    else:
		prosongidsbak.append(p)
	logging.debug('--prosongidsbak-----%s---',prosongidsbak)
	logging.debug('-----hasPromotion------%s---',hasPromotion)
	
	
	#if len(hasPromotion) == 0:
	#	return songinfos.values()	
	#else:


	for num in range(startIndex,limitNum+1):
              newOrderNo.append(num)
        	#生成新的排名
	logging.debug('========newOrderNo=start  %s===',newOrderNo)
	newOrderNo =  list(set(newOrderNo).difference(set(hasPromotion.values())))
	newOrderNo.sort()
	logging.debug('=========newOrderNo end =====%s===',newOrderNo)
	#newOrderNo.sort()
	#startsong = songinfoarray[newOrderNo[0] - 2]
        #endsong = songinfoarray[newOrderNo[0] - 1 ]
	i = 0

	songinfoarray.sort(cmp = sortByVirNum)	
	songinfoarray = calcOrderNo(songinfoarray)
	for song in songinfoarray:
		logging.debug('-------test song %s--------------',song)
	for songid in prosongidsbak:
		order_no = newOrderNo[i]
		startsong = songinfoarray[order_no-2]
		endsong = songinfoarray[order_no-1]
		logging.debug('order_no is %s --old song -  [%s] ----startsong--[%s]   endsong -- [%s]-' ,order_no,songinfos[songid],startsong ,endsong)
		
		newsong = getVirtualNum(songinfos[songid],startsong,endsong)
		#songinfoarray[index+1] = newsong
		songinfos[songid] = newsong
		logging.debug('----new song %s-------- ',songinfos[songid])
		songinfoarray = songinfos.values()
		songinfoarray.sort(cmp = sortByVirNum)
		songinfoarray = calcOrderNo(songinfoarray)
		for song in songinfoarray:
	                logging.debug('-------test pro songid %s-------songinfo-----%s--',songid,song)
		i = i+1
	for s in songinfos.values():
            if s.songid == 10165:
                logging.debug('the end  songinfo array is %s',s)

	return songinfoarray
			
	
		
		


	
#处理晋级的人员，你懂得。。。。
def processPromotionSong(db,resdict,prodict):
	actLimitDict = db.getActLimitSong()
	logging.info('the actLimitDict is %s ',actLimitDict)
	logging.info('the promotion dict info is %s',prodict)
        for k,v in resdict.items():
		#该活动下面有手工调整的晋`升人员
		if prodict.has_key(k) and len(prodict[k]) > 0 and actLimitDict.has_key(k):
			logging.debug('----------k is %s-----actLimitDict %s',k,actLimitDict)
			#该活动下的歌曲数需要大于设置的晋级总数
			proNum = len(prodict[k]) #该活动下面人工设置的需要晋级的人数
			limitNum = actLimitDict[k] #该活动下可以晋级的总歌曲数
			


			logging.info('the actid is %s,the promotion num is %s ,the limitnum is %s,the promotion songids is %s',k,proNum,limitNum,prodict[k])
		        #if proNum > actLimitDict[k]:
			dict = {}
			for r in v :
				dict[str(r.songid)] = r
			#startnum = limitNum - proNum
			#songlist = calcVirtualScore(startnum,startnum+1,v,prodict[k])
			resdict[k] = calcVirOrderNo(v,dict,limitNum,proNum,prodict[k])
			
			#debug
			for s in resdict[k]:
				if s.songid == 10176:
					logging.debug('------debug info------%s------',s) 
			#else:
			#logging.info('the activity (actid:%s), the promotion song num is %s,greater than the song num(%s)',proNum,actLimitDict[k],len(v))
		else:
			logging.info('the activity[actid:%s] has no promotion song or the match_no of the activity is not match ',k)	
	return resdict	


def sortByVirNum(self,other):
        if self.visible_rank_score > other.visible_rank_score:
                return -1
        elif self.visible_rank_score == other.visible_rank_score:
                if  self.visible_vote_num > other.visible_vote_num:
                        return -1
                elif self.visible_vote_num == other.visible_vote_num:
                        if self.visible_thumb_num > other.visible_thumb_num:
                                return -1
                        elif self.visible_thumb_num == other.visible_thumb_num:
                                if self.visible_listen_num > other.visible_listen_num:
                                        return -1
                                elif self.visible_listen_num <= other.visible_listen_num:
					 if self.matchsongid < other.matchsongid:
                                                        return -1
                                         elif self.matchsongid >= other.matchsongid:
                                                        return 1
                        else:
                                return 0
                else:
                        return 0
        else:
                return 0

        return -1

if __name__ == '__main__':






    
    db = dbutils.dbutils()


    hu = HttpUtils.HttpUtils()

    logging.debug('parse log finish ,the res is %s----------', dict )
    #定义一个resdict，key为活动id，value为该活动合并后的数组
    resdict = {}
    maxListenNumDict = {}
    actsongs = db.getActSongInfo() 	


	#select all activity from db
    for k,matchsong in actsongs.items():
	logging.debug('the  activity (actid :%s) songinfos (select from db) is %s',k,matchsong)
	info = k.split(',')
	topicid = info[0]
	actid = info[1]
	songid = info[2]

	thumbNum = 0
        maxThumbNum = 0
        voteNum = 0
        maxVoteNum = 0
        maxListenNum = 0

	listen_score = 0
	thumb_score = 0
        vote_score = 0

        thumbDict = parseHttpResult(hu.getHttpReq('collect',topicid+'_'+actid))
        if thumbDict.has_key(songid):
                thumbNum = thumbDict[songid]
        if len(thumbDict.values()) > 0 :
                maxThumbNum = max(thumbDict.values())

        voteDict = parseHttpResult(hu.getHttpReq('vote',topicid+'_'+actid))
        if voteDict.has_key(songid):
                voteNum = voteDict[songid]
        if len(voteDict.values()) > 0 :
                maxVoteNum = max(voteDict.values())


	#matchsong = null 
	logging.debug('select the song(%s) info from db',k)	
	matchsong.visible_listen_num = matchsong.listen
	

	matchsong.vote = voteNum
	matchsong.thumb = thumbNum

	maxListenNum = getActivityNum(db,actid)


	vote_score = calcScore(db,actid,maxVoteNum,voteNum,Acts.VOTE,songid)
	thumb_score = calcScore(db,actid,maxThumbNum,thumbNum,Acts.THUMB,songid)
        listen_score = calcScore(db,actid,maxListenNum,matchsong.listen,Acts.LISTEN,songid)
	total_score = float(thumb_score) + float(vote_score) + float(listen_score)

	matchsong.vote_score = vote_score
	matchsong.collect_score = thumb_score
        matchsong.visible_vote_score = float(vote_score)
        matchsong.visible_collect_score = float(thumb_score)
	matchsong.visible_listen_score = float(listen_score)

	matchsong.score = total_score
	matchsong.visible_rank_score = total_score 
        matchsong.visible_vote_num = voteNum
        matchsong.visible_thumb_num = thumbNum 
	#logging.debug('select from db ,songid %s--thumb_score %s-----vote_score %s--listen_score %s  ,total_score-%s ',songid,thumb_score,vote_score,listen_score,matchsong.score)



	logging.info('calc collect and vote finished ,activity id %s ,max thumb num is %s, max vote num is %s , the song[id:%s] thumb num is  %s,vote num is %s,the listen num is %s,the thumb score is %s ,the vote score is %s',actid,maxThumbNum,maxVoteNum,songid,thumbNum,voteNum,matchsong.listen,thumb_score,vote_score)
	
	if resdict.has_key(actid):
                 resdict[actid].append(matchsong)
        else:
                 tmplist = []
                 tmplist.append(matchsong)
                 resdict[actid] = tmplist

    logging.info('calc the activity max listennum , the result is %s',maxListenNumDict)




    #对每个活动的所有歌曲进行排序,具体的重构规则在matchsong表的cmp函数中实现
    for k,v in resdict.items():
	v.sort()
	#排过序的集合,修改排序字段
	j = 0
	for i in v :
		j =j + 1
		i.order_no = j
		logging.info('calc score finished,the result is %s',i)

	
  
    pdict = getProSongs(actsongs)

    
    
    resdict = processPromotionSong(db,resdict,pdict) 
	




	
	 #排过序的集合,修改排序字段
    for actid ,songinfos in resdict.items():
	songinfos.sort(cmp = sortByVirNum)
	j = 0
        for i in songinfos :
                j =j + 1
                i.order_no = j
		logging.info('begin to update the last  matchsonginfo to db , the info is %s',i)
		db.updateSongInfo(str(actid),i)

    
		
		
	   



