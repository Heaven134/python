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


Acts = enum(THUMB=1, VOTE=2, LISTEN=3,LISTEN_GOOD=4,LISTEN_NORMAL=5,LISTEN_BAD=6,LISTEN_GOOD_OTHER=7,LISTEN_NORMAL_OTHER=8,LISTEN_BAD_OTEHR=9)


def parseHeyinliangLog():
        u1 = r"?P<u1>\S+"
        u2 = r"?P<u2>\S+"
        u3 = r"?P<u3>\S+"
        u4 = r"?P<u4>\S+"
        u5 = r"?P<u5>\S+"
        u6 = r"?P<u6>\S+"
        u7 = r"?P<u7>\S+"
        u8 = r"?P<u8>\S+"
        u9 = r"?P<u9>\S+"
        u10 = r"?P<u10>\S+"
        u11= r"?P<u11>\S+"
        u12 = r"?P<u12>\S+"
        u13 = r"?P<u13>\S+"
        info = r"?P<info>\S+"
        


def parselog():



        u1 = r"?P<u1>\S+"
        u2 = r"?P<u2>\S+"
        u3 = r"?P<u3>\S+"
        u4 = r"?P<u4>\S+"
        u5 = r"?P<u5>\S+"
        u6 = r"?P<u6>\S+"
        u7 = r"?P<u7>\S+"
        u8 = r"?P<u8>\S+"
        u9 = r"?P<u9>\S+"
        u10 = r"?P<u10>\S+"
        u11= r"?P<u11>\S+"
        u12 = r"?P<u12>\S+"
        u13 = r"?P<u13>\S+"
        info = r"?P<info>\S+"


        p = re.compile(r"(%s)\ (%s)\ (%s)\ (%s)\ (%s)\ (%s)\ (%s)\ (%s)\ (%s)\ (%s)\ (%s)\ (%s)\ (%s)\ (%s).*?" %(u1,u2,u3,u4,u5,u6,u7,u8,u9,u10,u11,u12,u13,info), re.VERBOSE)
        
        listen_log_path = config['listen_log_path']
        lasthour = ((datetime.datetime.now()-datetime.timedelta(hours=1)).strftime("%Y%m%d%H"))
        listen_log_path = listen_log_path % lasthour
        if os.path.isfile(listen_log_path) == False:
            logging.error('the listen_log_path [%s] no exist',listen_log_path)
            sys.exit(1) 
            return
        else:
            logging.info('begin to parse log info %s ',listen_log_path) 

        logfile=open(listen_log_path)
        listendict = {}
        while True:
            line = logfile.readline()
            if not line:
                break
            if 'log_song_play' not in line :
                continue
            info = line.split(' ')[15]
            #logging.debug('parse log , the info is %s' , info)
            info = info.replace('log[','').replace(']','')
        
            logs = info.split('_')
            #logging.debug('parse ,the parsed log info is %s',logs)
            topicid = logs[0]
            actid = logs[1]
            songid = logs[2]
            userid = logs[3]
            userlevel = logs[4]
        
            key = topicid+','+ actid+','+songid
            if listendict.has_key(key)        :
                listendict[key]=listendict[key]+1
            else:
                listendict[key] = 1                
                        #print 'not contains'
        logging.info('parse log %s finish,the  result of the listen num is %s',listen_log_path,listendict)
        return listendict


def parserequest(rqst):
    param = r"?P<param>.*"
    p = re.compile(r"/play\?(%s)" %param, re.VERBOSE)
    param = re.findall(p, rqst)
    #print '---------------------------------',param,rqst
    ps = param[0].split("&")
    dict = {}
    for i in ps:
        #print '============',i,i.split("=")[0],i.split("=")[1]
        #p = i.split("=")
        #print p
        dict[i.split("=")[0]] = i.split("=")[1]

    #print '-----------------',dict

    return dict
#获取一个活动的所有的点赞的信息
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
                elif type == Acts.LISTEN_GOOD:
                    return res['quantity_1_ratio']
                elif type == Acts.LISTEN_NORMAL:
                    return res['quantity_2_ratio']
                elif type == Acts.LISTEN_BAD:
                    return res['quantity_3_ratio']
                elif type == Acts.LISTEN_GOOD_OTHER:
                    return res['quantity_4_ratio']
                elif type == Acts.LISTEN_NORMAL_OTHER:
                    return res['quantity_5_ratio']
                elif type == Acts.LISTEN_BAD_OTEHR:
                    return res['quantity_6_ratio']
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
#        #print '----url--------',url
#        r = random.randint(10, 20)
#        obj = { 'error_code': 22000, 'result': [ { url: { 'num':  } } ] }
#        return obj
#            #conn = httplib.HTTPConnection(url)
#        #conn.request('get', '/')
#        #res = conn.getresponse().read()
#        #conn.close()
#        #return res 
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
        if (maxnum) == 0 or int(num) == 0:
                res = 0
        elif int(maxnum) == int(num):
                res = base
        else:
                r = math.log(float(num))/math.log(float(maxnum))*base
                res = '{:.2f}'.format(Decimal(r))  
        logging.info('begin to calc score,type is %s , base is %s ,the songid is %s ,the maxnum is %s,and the current num is %s,and the score is %s',type,base,songid,maxnum,num,res ) 
        return res  
def calcNumScore(db,actid,num,type,songid = 0):
        logging.debug('calcScore ,the actid is %s ,num is %s ',actid,num)
        base = getRatio(db,actid,type)
        if base == 0:
                return 0

        res = 0
        if int(num) == 0:
                res = 0
        else:
                res = num*base
                #res = '{:.2f}'.format(Decimal(r))  
        logging.info('begin to calc score,type is %s , base is %s ,the songid is %s , the current num is %s,and the score is %s',type,base,songid,num,res ) 
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
#        logging.info('update the song score ,the songid is %s,and the socre is %s ',songid,score)
#        db = dbutils.dbutils(dblib.Mysql(config['dbconf']))
#        db.updateSongScore(songid,score);
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

        f = (startsong.visible_rank_score - 0.01) == endsong.visible_rank_score or (startsong.visible_rank_score == endsong.visible_rank_score)

        logging.debug('get the virtual score and num ,the songinfo is [%s],the startsong  info is [%s] ,the endsong info is [%s],the com res is [%s]',songinfo,startsong,endsong,f)

        #正常情况下，分数-0.01
        #if f: 
        #if (startsong.visible_rank_score - 0.01) == endsong.visible_rank_score or (startsong.visible_rank_score == endsong.visible_rank_score):
        #        logging.debug('the visible_rank_score of the start song [%s] and the end song[%s]  is same ',startsong,endsong)
        #        songinfo.visible_rank_score = startsong.visible_rank_score 
        #else:
        songinfo.visible_rank_score = startsong.visible_rank_score 
        songinfo.visible_vote_num = startsong.visible_vote_num 
        songinfo.visible_listen_num = startsong.visible_listen_num
        songinfo.visible_thumb_num = startsong.visible_thumb_num

        #if startsong.visible_listen_score != 0:
        songinfo.visible_listen_score = startsong.visible_listen_score 
        songinfo.visible_collect_score = startsong.visible_collect_score
        songinfo.visible_vote_score = startsong.visible_vote_score
        #elif startsong.visible_listen_score == 0 and startsong.visible_collect_score != 0:
        #        songinfo.visible_listen_score = startsong.visible_listen_score 
        #        songinfo.visible_collect_score = startsong.visible_collect_score - 0.01
        #        songinfo.visible_vote_score = startsong.visible_vote_score
        #elif startsong.visible_collect_score == 0 and startsong.visible_vote_score != 0:
        #        songinfo.visible_listen_score = startsong.visible_listen_score 
        #        songinfo.visible_collect_score = startsong.visible_collect_score 
        #        songinfo.visible_vote_score = startsong.visible_vote_score - 0.01


        #else:
        #    if (startsong.visible_vote_num + 1) < endsong.visible_vote_num :
        #        songinfo.visible_rank_score = startsong.visible_rank_score 
        #        songinfo.visible_vote_num = startsong.visible_vote_num - 1
        #        songinfo.visible_listen_num = startsong.visible_listen_num
        #        songinfo.visible_thumb_num = startsong.visible_thumb_num



        #        #投票量相同的情况下，点赞数+1
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
                                
#def calcVirOrderNo(songinfoarray,songinfos,limitNum,proNum,prosongids):
#        
#        if len(songinfoarray) < limitNum:
#                return songinfoarray
#        
#        #for s in songinfos.values():
#        #     if s.songid == 10165:
#        #        logging.debug('the ori songinfo array is %s',s)
#        newOrderNo = []
#
#        hasPromotion = {}
#        startIndex = limitNum-proNum + 1
#        
#        logging.info('the limitNum is %s,the pronum is %s',limitNum,proNum)
#        for p in prosongids:
#            if songinfos[p].order_no <= limitNum:
#                hasPromotion[songinfos[p].songid] = songinfos[p].order_no
#                #如果该歌曲的排名已经晋级，将不再处理,将其从待晋级的歌曲列表中移除
#                if songinfos[p].order_no < (limitNum-proNum + 1):
#                        startIndex = startIndex + 1
#                        prosongids.remove(p)
#                        logging.info('the song[songid:%s,real orderno:%s] has promotioned ,remove id from promotion list',songinfos[p],songinfos[p].order_no)
#                elif songinfos[p].order_no >= (limitNum-proNum + 1):
#                        startIndex = startIndex - 1
#        logging.debug('---prosongids-----%s---',prosongids)
#        logging.debug('-----hasPromotion------%s---',hasPromotion)
#        
#        
#        #if len(hasPromotion) == 0:
#        #        return songinfos.values()        
#        #else:
#
#
#        for num in range(startIndex,limitNum+1):
#              newOrderNo.append(num)
#                #生成新的排名
#        logging.debug('========newOrderNo=start  %s===',newOrderNo)
#        newOrderNo =  list(set(newOrderNo).difference(set(hasPromotion.values())))
#        newOrderNo.sort()
#        logging.debug('=========newOrderNo end =====%s===',newOrderNo)
#        #newOrderNo.sort()
#        #startsong = songinfoarray[newOrderNo[0] - 2]
#        #endsong = songinfoarray[newOrderNo[0] - 1 ]
#        i = 0
#
#        songinfoarray.sort(cmp = sortByVirNum)        
#        songinfoarray = calcOrderNo(songinfoarray)
#        for song in songinfoarray:
#                logging.debug('-------test song %s--------------',song)
#        for songid in prosongids:
#                order_no = newOrderNo[i]
#                startsong = songinfoarray[order_no-2]
#                endsong = songinfoarray[order_no-1]
#                logging.debug('order_no is %s --old song -  [%s] ----startsong--[%s]   endsong -- [%s]-' ,order_no,songinfos[songid],startsong ,endsong)
#                
#                newsong = getVirtualNum(songinfos[songid],startsong,endsong)
#                #songinfoarray[index+1] = newsong
#                songinfos[songid] = newsong
#                logging.debug('----new song %s-------- ',songinfos[songid])
#                songinfoarray = songinfos.values()
#                songinfoarray.sort(cmp = sortByVirNum)
#                songinfoarray = calcOrderNo(songinfoarray)
#                for song in songinfoarray:
#                        logging.debug('-------test pro songid %s-------songinfo-----%s--',songid,song)
#                i = i+1
#        for s in songinfos.values():
#            if s.songid == 10165:
#                logging.debug('the end  songinfo array is %s',s)
#
#        return songinfoarray
                        
        
def calcVirOrderNo(songinfoarray,songinfos,limitNum,proNum,prosongids):

        if len(songinfoarray) < limitNum:
                return songinfoarray

        #for s in songinfos.values():
        #     if s.songid == 10165:
        #       logging.debug('the ori songinfo array is %s',s)
        newOrderNo = []

        hasPromotion = {}
        startIndex = limitNum-proNum+1

        logging.info('the limitNum is %s,the pronum is %s,the promotion songids is %s',limitNum,proNum,prosongids)
        prosongidsbak = []
        for p in prosongids:
            logging.info('the promotion song (%s) info is %s',p,songinfos[p])
            if songinfos[p].order_no <= limitNum:
                #如果该歌曲的排名已经晋级，将不再处理,将其从待晋级的歌曲列表中移除
                if songinfos[p].order_no <= limitNum-proNum+1 :
                        hasPromotion[songinfos[p].songid] = songinfos[p].order_no
                        startIndex = startIndex + 1
                        logging.info('the song[songid:%s,real orderno:%s] has promotioned ,remove id from promotion list,startIndex ++ ',songinfos[p],songinfos[p].order_no)
                elif songinfos[p].order_no > limitNum-proNum+1:
                        logging.info('the song[songid:%s,real orderno:%s] need to deal by head,startIndex--',songinfos[p],songinfos[p].order_no)
                        prosongidsbak.append(p)
                        #startIndex = startIndex - 1
            else:
                prosongidsbak.append(p)
        logging.debug('the promotion song len is %s,and the songinfo is %s',len(prosongidsbak),prosongidsbak)
        logging.debug('hasPromotion songid length is %s, and the ids is ------%s---',len(hasPromotion),hasPromotion)


        startIndex = startIndex - 2
        if startIndex < 0:
            startIndex = 0
        startsong = songinfoarray[startIndex]
        logging.debug('the startIndex is %s,the start song is %s',startIndex,startsong)
        for songid in prosongidsbak:
                songinfos[songid].visible_rank_score = startsong.visible_rank_score
                songinfos[songid].visible_vote_num = startsong.visible_vote_num
                songinfos[songid].visible_listen_num = startsong.visible_listen_num
                songinfos[songid].visible_thumb_num = startsong.visible_thumb_num
         
                songinfos[songid].visible_listen_score = startsong.visible_listen_score
                songinfos[songid].visible_collect_score = startsong.visible_collect_score
                songinfos[songid].visible_vote_score = startsong.visible_vote_score
                
                
                songinfos[songid].visible_score_1 = startsong.visible_score_1
                songinfos[songid].visible_score_2 = startsong.visible_score_2
                songinfos[songid].visible_score_3 = startsong.visible_score_3
                songinfos[songid].visible_score_4 = startsong.visible_score_4
                songinfos[songid].visible_score_5 = startsong.visible_score_5
                songinfos[songid].visible_score_6 = startsong.visible_score_6
            
        songinfoarray = songinfos.values()
        songinfoarray.sort(cmp = sortByVirNum)


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

        


        
        #改了算法，这个段代码用不着了，先留着。
        #songinfoarray.sort(cmp = sortByVirNum)
        #songinfoarray = calcOrderNo(songinfoarray)
        ##for song in songinfoarray:
        ##        logging.debug('-------test song %s--------------',song)
        #for songid in prosongidsbak:
        #        order_no = newOrderNo[i]
        #        startsong = songinfoarray[order_no-2]
        #        endsong = songinfoarray[order_no-1]
        #        logging.debug('order_no is %s --old song -  [%s] ----startsong--[%s]   endsong -- [%s]-' ,order_no,songinfos[songid],startsong ,endsong)

        #        newsong = getVirtualNum(songinfos[songid],startsong,endsong)
        #        #songinfoarray[index+1] = newsong
        #        songinfos[songid] = newsong
        #        logging.debug('----new song %s-------- ',songinfos[songid])
        #        songinfoarray = songinfos.values()
        #        songinfoarray.sort(cmp = sortByVirNum)
        #        songinfoarray = calcOrderNo(songinfoarray)
        #        for song in songinfoarray:
        #                logging.debug('-------test pro songid %s-------songinfo-----%s--',songid,song)
        #        i = i+1

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
                if  self.visible_vote_score > other.visible_vote_score:
                        return -1
                elif self.visible_vote_score == other.visible_vote_score:
                        if self.visible_collect_score > other.visible_collect_score:
                                return -1
                        elif self.visible_collect_score == other.visible_collect_score:
                                if self.visible_listen_score > other.visible_listen_score:
                                        return -1
                                elif self.visible_listen_score == other.visible_listen_score:
                                    if self.visible_score_1 > other.visible_score_1:
                                            return -1
                                    elif self.visible_score_1 == other.visible_score_1:
                                        if self.visible_score_4 > other.visible_score_4:
                                            return -1
                                        elif self.visible_score_4 == other.visible_score_4:
                                            if self.visible_score_3 > other.visible_score_3:
                                                return -1
                                            elif self.visible_score_3 == other.visible_score_3:
                                                if self.visible_score_6 > other.visible_score_6:
                                                    return -1
                                                elif self.visible_score_6 == other.visible_score_6:
                                                    if self.visible_score_2 > other.visible_score_2:
                                                        return -1
                                                    elif self.visible_score_2 == other.visible_score_2:
                                                        if self.visible_score_5 > other.visible_score_5:
                                                            return -1
                                                        elif self.visible_score_5 == other.visible_score_5:
                                                            if self.promotion > other.promotion:
                                                                return -1
                                                            elif self.promotion == other.promotion:
                                                                if self.matchsongid < other.matchsongid:
                                                                    return -1
                                                                elif self.matchsongid >= other.matchsongid:
                                                                    return 1
                                                            else:
                                                                return 1
                                                        else:
                                                            return 1
                                                    else:
                                                        return 1
                                                else:
                                                    return 1
                                            else:
                                                return 1
                                        else:
                                            return 1
                                    else:
                                        return 1
                                else:
                                    return 1
                        else:
                                return 0
                else:
                        return 0
        else:
                return 0

        return -1

def addMaxNum(dict,actid,listennum):
        logging.debug('add max num ,the dict is %s',dict)
        actid = str(actid)
        if dict.has_key(actid):
            if listennum > dict[actid]:
                dict[actid] = listennum
        else:
            dict[actid]=listennum    
if __name__ == '__main__':





    #print config['dbconf']
    #print "你好"
    #r = redis.Redis(host='localhost',port=6379,db=0)
    #gd = dbutils.dbutils(dblib.Mysql(config['dbconf']),r)
    #gd.insertSongLog();
    #gd.getDefaultList() 
    #print "end"
    #main()

    #setLogInfo()

    #解析日志
    listendict = parselog()
    if listendict is None:
        logging.info('parse log error , exit !')
        sys.exit(0)
    #logging.info('parse log finish,the  result of the listen num is %s',listendict)

    #调用接口获取投票量和点赞数
    #print  listendict.items()
    
    db = dbutils.dbutils()
    dict = {}


    hu = HttpUtils.HttpUtils()

        
    for k,listennum in listendict.items():
        r = k.split(",")
        topicid = r[0]
        activityid = r[1]
        songid = r[2]
        

        #将解析后的数据放到dict里,用于下面的合并操作        
        tmpdict = {}
        tmpdict['listenNum']= listennum
        dict[topicid+','+activityid+','+songid] = tmpdict



                        
   
     
    logging.debug('parse log finish ,the res is %s----------', dict )
    #定义一个resdict，key为活动id，value为该活动合并后的数组
    resdict = {}
    maxListenNumDict = {}
    maxVoteNumDict = {}
    maxCollectNumDict = {}
    maxQuantity_1_Dict = {}
    maxQuantity_2_Dict = {}
    maxQuantity_3_Dict = {}
    maxQuantity_4_Dict = {}
    maxQuantity_5_Dict = {}
    maxQuantity_6_Dict = {}
    actsongs = db.getActSongInfo()         
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
        
        
        quantity_1_num=0
        quantity_2_num=0
        quantity_3_num=0
        quantity_4_num=0
        quantity_5_num=0
        quantity_6_num=0
        
        quantity_1_score=0
        quantity_2_score=0
        quantity_3_score=0
        quantity_4_score=0
        quantity_5_score=0
        quantity_6_score=0

        thumbDict = parseHttpResult(hu.getActsong('collect',topicid+'_'+actid,songid))
        if thumbDict.has_key(songid):
                thumbNum = thumbDict[songid]
                matchsong.thumb = thumbNum
                matchsong.visible_thumb_num = thumbNum
                addMaxNum(maxCollectNumDict,actid,thumbNum)
        #if len(thumbDict.values()) > 0 :
        #        maxThumbNum = max(thumbDict.values())

        voteDict = parseHttpResult(hu.getActsong('vote',topicid+'_'+actid,songid))
        if voteDict.has_key(songid):
                voteNum = voteDict[songid]
                matchsong.vote = voteNum
                matchsong.visible_vote_num = voteNum
                addMaxNum(maxVoteNumDict,actid,voteNum)
        #if len(voteDict.values()) > 0 :
        #        maxVoteNum = max(voteDict.values())
        #        matchsong.thumb = thumbNum

        #maxListenNum = getActivityNum(db,actid)
        
        
        quantity_1_Dict = parseHttpResult(hu.getActsong('listengood',topicid+'_'+actid,songid))
        if quantity_1_Dict.has_key(songid):
                quantity_1_num = quantity_1_Dict[songid]
                matchsong.visible_quantity_1 = quantity_1_num
                addMaxNum(maxQuantity_1_Dict,actid,quantity_1_num)
        quantity_2_Dict = parseHttpResult(hu.getActsong('listennormal',topicid+'_'+actid,songid))
        if quantity_2_Dict.has_key(songid):
                quantity_2_num = quantity_2_Dict[songid]
                matchsong.visible_quantity_2 = quantity_2_num
                addMaxNum(maxQuantity_2_Dict,actid,quantity_2_num)
        quantity_3_Dict = parseHttpResult(hu.getActsong('listenbad',topicid+'_'+actid,songid))
        if quantity_3_Dict.has_key(songid):
                quantity_3_num = quantity_3_Dict[songid]
                matchsong.visible_quantity_3 = quantity_3_num
                addMaxNum(maxQuantity_3_Dict,actid,quantity_3_num)
        quantity_4_Dict = parseHttpResult(hu.getActsong('listengoodother',topicid+'_'+actid,songid))
        if quantity_4_Dict.has_key(songid):
                quantity_4_num = quantity_4_Dict[songid]
                matchsong.visible_quantity_4 = quantity_4_num
                addMaxNum(maxQuantity_4_Dict,actid,quantity_4_num)
        quantity_5_Dict = parseHttpResult(hu.getActsong('listennormalother',topicid+'_'+actid,songid))
        if quantity_5_Dict.has_key(songid):
                quantity_5_num = quantity_5_Dict[songid]
                matchsong.visible_quantity_5 = quantity_5_num
                addMaxNum(maxQuantity_5_Dict,actid,quantity_5_num)
        quantity_6_Dict = parseHttpResult(hu.getActsong('listenbadother',topicid+'_'+actid,songid))
        if quantity_6_Dict.has_key(songid):
                quantity_6_num = quantity_6_Dict[songid]
                matchsong.visible_quantity_6 = quantity_6_num
                addMaxNum(maxQuantity_6_Dict,actid,quantity_6_num)


        #matchsong = null 
        if dict.has_key(k):
                listenNum = matchsong.listen 
                matchsong.listen = listenNum + dict[k]['listenNum'] #新的试听量等于数据库的试听量加上新解析出来的试听量
                matchsong.visible_listen_num = matchsong.listen
                #强制将歌曲试听变为0，注意之后可能会改
                matchsong.listen = 0
                matchsong.visible_listen_num = 0
                addMaxNum(maxListenNumDict,actid,matchsong.listen)
                logging.info('the song (%s) selected from db exist the logs,the listen num is %s ',k,matchsong.listen)
        else:
                logging.debug('select the song(%s) info from db',k)        
                matchsong.visible_listen_num = matchsong.listen
                #强制将歌曲试听变为0，注意之后可能会改
                matchsong.listen = 0
                matchsong.visible_listen_num = 0
                addMaxNum(maxListenNumDict,actid,matchsong.listen)
        



        #vote_score = calcScore(db,actid,maxVoteNum,voteNum,Acts.VOTE,songid)
        #thumb_score = calcScore(db,actid,maxThumbNum,thumbNum,Acts.THUMB,songid)
        #listen_score = calcScore(db,actid,maxListenNum,matchsong.listen,Acts.LISTEN,songid)
        #total_score = float(thumb_score) + float(vote_score)

        #matchsong.vote_score = vote_score
        #matchsong.collect_score = thumb_score
        #matchsong.visible_vote_score = float(vote_score)
        #matchsong.visible_collect_score = float(thumb_score)


        #matchsong.score = total_score
        #matchsong.visible_rank_score = total_score 
        #matchsong.visible_vote_num = voteNum
        #matchsong.visible_thumb_num = thumbNum 
        #logging.debug('select from db ,songid %s--thumb_score %s-----vote_score %s--listen_score %s  ,total_score-%s ',songid,thumb_score,vote_score,listen_score,matchsong.score)



        logging.info('calc song num  finished ,activity id %s , the song[id:%s] thumb num is  %s,vote num is %s,the listen num is %s',actid,songid,thumbNum,voteNum,matchsong.listen)
        
        if resdict.has_key(actid):
                 resdict[actid].append(matchsong)
        else:
                 tmplist = []
                 tmplist.append(matchsong)
                 resdict[actid] = tmplist

    logging.info('calc the activity max num  finished , the listen max result is %s,the vote max result is %s ,the collect max result is %s ',maxListenNumDict,maxVoteNumDict,maxCollectNumDict)


    #logging.info('calc num finished ,the resdict result is %s',resdict)

    #最大的试听量需要根据日志和数据库里的数据联合算出来
    for actid,matchsongs in resdict.items():
        actid = str(actid)
        maxListenNum = 0 
        maxVoteNum = 0
        maxCollectNum = 0
        
        maxQuantity_1_num = 0
        maxQuantity_2_num = 0
        maxQuantity_3_num = 0
        maxQuantity_4_num = 0
        maxQuantity_5_num = 0
        maxQuantity_6_num = 0

        if maxListenNumDict.has_key(actid):
                maxListenNum = maxListenNumDict[actid]
        if maxVoteNumDict.has_key(actid):
                maxVoteNum = maxVoteNumDict[actid]
        if maxCollectNumDict.has_key(actid):
                maxCollectNum = maxCollectNumDict[actid]
        if maxQuantity_1_Dict.has_key(actid):
            maxQuantity_1_num = maxQuantity_1_Dict[actid]
        if maxQuantity_2_Dict.has_key(actid):
            maxQuantity_2_num = maxQuantity_2_Dict[actid]
        if maxQuantity_3_Dict.has_key(actid):
            maxQuantity_3_num = maxQuantity_3_Dict[actid]
        if maxQuantity_4_Dict.has_key(actid):
            maxQuantity_4_num = maxQuantity_4_Dict[actid]
        if maxQuantity_5_Dict.has_key(actid):
            maxQuantity_5_num = maxQuantity_5_Dict[actid]
        if maxQuantity_6_Dict.has_key(actid):
            maxQuantity_6_num = maxQuantity_6_Dict[actid]

        for matchsong in matchsongs:
            listen_score = calcScore(db,actid,maxListenNum,matchsong.listen,Acts.LISTEN,matchsong.songid)        
            vote_score = calcScore(db,actid,maxVoteNum,matchsong.vote,Acts.VOTE,matchsong.songid)
            thumb_score = calcScore(db,actid,maxCollectNum,matchsong.thumb,Acts.THUMB,matchsong.songid)
            
            
            quantity_1_score = calcNumScore(db,actid,matchsong.visible_quantity_1,Acts.LISTEN_GOOD,matchsong.songid)
            quantity_2_score = calcNumScore(db,actid,matchsong.visible_quantity_2,Acts.LISTEN_NORMAL,matchsong.songid)
            quantity_3_score = calcNumScore(db,actid,matchsong.visible_quantity_3,Acts.LISTEN_BAD,matchsong.songid)
            quantity_4_score = calcNumScore(db,actid,matchsong.visible_quantity_4,Acts.LISTEN_GOOD_OTHER,matchsong.songid)
            quantity_5_score = calcNumScore(db,actid,matchsong.visible_quantity_5,Acts.LISTEN_NORMAL_OTHER,matchsong.songid)
            quantity_6_score = calcNumScore(db,actid,matchsong.visible_quantity_6,Acts.LISTEN_BAD_OTEHR,matchsong.songid)
            
            matchsong.visible_score_1 = quantity_1_score
            matchsong.visible_score_2 = quantity_2_score
            matchsong.visible_score_3 = quantity_3_score
            matchsong.visible_score_4 = quantity_4_score
            matchsong.visible_score_5 = quantity_5_score
            matchsong.visible_score_6 = quantity_6_score
        
            matchsong.listen_score = listen_score        
            matchsong.vote_score = vote_score
            matchsong.collect_score = thumb_score

            matchsong.visible_vote_score = float(vote_score)
            matchsong.visible_collect_score = float(thumb_score)
            matchsong.visible_listen_score = float(listen_score)

            total_score = float(vote_score) + float(listen_score) + float(thumb_score) + float(quantity_1_score) + float(quantity_2_score) + float(quantity_3_score) + float(quantity_4_score) + float(quantity_5_score) + float(quantity_6_score)
            
            matchsong.score = total_score
            matchsong.visible_rank_score = total_score 
            logging.info('calc  score finished,activity id %s ,max listen num is %s,max vote num is %s,max collect max num is %s, the song[id:%s],the listen num is %s,the listen score is %s ,the vote num is %s,the vote score is %s,the collect num is %s,the collect score is %s,and the total score is %s',matchsong.actid,maxListenNum,maxVoteNum,maxCollectNum,matchsong.songid,matchsong.listen,listen_score,matchsong.vote,vote_score,matchsong.thumb,thumb_score,total_score)





    #logging.info('resdict is %s',resdict)

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
    #for actid,songinfos in resdict.items():
    #    thumbDict = parseHttpResult(getHttpReq('thumb',actid))
    #    voteDict = parseHttpResult(getHttpReq('vote',actid))
    #    maxListenNum = getActivityNum(db,activityid)
    #    maxThumbNum = 0 
    #    maxVoteNum = 0         

    #    for song in songinfos:
    #        if len(thumbDict) > 0:        
    #            if thumbDict.has_key(song.songid):
    #                    thumbNum = thumbDict[song.songid]
    #            maxThumbNum = max(thumbDict.values())
    #             if len(voteDict) > 0:
    #            if voteDict.has_key(song.songid):
    #                    voteNum = voteDict[song.songid]
    #            maxVoteNum = max(voteDict.values())


    #        listen_score = calcScore(maxListenNum,song.visible_listen_num,Acts.LISTEN)
    #        thumb_score = calcScore(maxThumbNum,song.visible_thumb_num,Acts.THUMB)
    #        vote_score = calcScore(maxVoteNum,song.visible_vote_num,Acts.VOTE)
    #    
    #        visible_total_score = float(listen_score) + float(thumb_score) + float(vote_score)
    #        song.visible_rank_score = visible_total_score
                
        




        #v.sort(cmp = sortByVirNum)
        
         #排过序的集合,修改排序字段
    for actid ,songinfos in resdict.items():
        songinfos.sort(cmp = sortByVirNum)
        j = 0
        for i in songinfos :
                j =j + 1
                i.order_no = j
                logging.info('begin to update the last  matchsonginfo to db , the info is %s',i)
                db.updateSongInfo(str(actid),i)

    
                
                
           



