#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import os    

WORK_NODE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# print CURRENT_DIR
os.sys.path.insert(0, os.path.dirname(WORK_NODE_DIR))

import random
from src.cores import matchsong
from src.cores import dblib
from src.conf import config
from src.cores import my_logger as logging


class dbutils:
    def __init__(self):
	#print '------------',config['dbconf']	

        self.db = dblib.Mysql(config['dbconf'])
	
	#self.r=redis
    #获取详细列表
    def getDefaultList(self):
        sql = "select song_id from  he_songs_info"
        record = self.db.getAll(sql)         
	#print len(record)
	songids = []
	for r in record:
	    	songids.append(r['song_id'])
	    	#print r['song_id']
	random.shuffle(songids)
        res = chunks(songids,2)
	print '-------------',res,len(res)	
	for idx,val in enumerate(res):
	    print '-==========',idx,val
	    self.r.set('detail_'+bytes(idx),val)
	print self.r.get('test')
	#print songids
    def insertSongLog(self):
	sql="insert into he_activity_match_songs(topic_id,activity_id,song_id,user_id,user_name,match_no,listen_num,rank_score,order_no,suggest) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) "
        values = (1,1,1,1,1,1,1,1,1,1)
	self.db.insertOne(sql,values)
    def getActivityNum(self):
	sql = 'SELECT  m.activity_id , max(listen_num)  maxlistennum  FROM  he_activity_match_songs m join he_activity a on m.activity_id = a.activity_id where m.match_no = a.match_no  GROUP BY activity_id'	
	record = self.db.getAll(sql)
	res = {}
	for r in record:
		res[r['activity_id']]=r['maxlistennum']	
	return res
    def updateSongScore(self,songid,score):
	sql = 'update he_activity_match_songs set rank_score  = %s where song_id  = %s'
	return self.db.update(sql,(score,songid))

    #每个活动取top200
    def getTopSong(self):
        sql = '''

        	SELECT *
        	FROM
        	  (SELECT b.*,
        	          (CASE b.activity_id WHEN @curType THEN @curRow := @curRow + 1 ELSE @curRow := 1
        	           AND @curType := b.activity_id END) AS rank
        	   FROM
        	     (SELECT song_id,
        	             p.topic_id,
        	             p.activity_id,
        	             visible_rank_score
        	      FROM he_activity_match_songs p
        	      JOIN he_activity a ON (a.activity_id = p.activity_id
        	                                  AND a.match_no = p.match_no
        	                                  AND a.status = 1
        	                                  AND a.match_no > 0)
        	      ORDER BY p.activity_id,
        	               visible_rank_score DESC) b ,
        	     (SELECT @curRow := 0, @curType := 0) r) c
        	WHERE c.rank <= 200
        
        	'''

        record = self.db.getAll(sql)
        return record
    def getNotTopSong(self):
	sql = '''
		SELECT *
		FROM
		  (SELECT b.*,
		          (CASE b.activity_id WHEN @curType THEN @curRow := @curRow + 1 ELSE @curRow := 1
		           AND @curType := b.activity_id END) AS rank
		   FROM
		     (SELECT song_id,
		             p.topic_id,
		             p.activity_id,
		 	     visible_rank_score
		      FROM he_activity_match_songs p
		      JOIN he_activity a ON (a.activity_id = p.activity_id
		                                  AND a.match_no = p.match_no
		                                  AND a.status = 1
		                                  AND a.match_no > 0)
		      ORDER BY p.activity_id,
		               visible_rank_score DESC) b ,
		     (SELECT @curRow := 0, @curType := 0) r) c
			WHERE c.rank > 200

	
		'''


        record = self.db.getAll(sql)
	dict = {}
	if record !=False:
	    for r in record:
        	topicid = r['topic_id']
        	actid = r['activity_id']
        	songid = r['song_id']
		key = str(topicid) + '_' + str(actid)
		if dict.has_key(key):
			dict[key].append(songid)
		else:
			dict[key] = [songid]
        return dict

    def getSuggestSong(self):
	sql = '''
		
		SELECT b.*,
				(CASE b.activity_id WHEN @curType THEN @curRow := @curRow + 1 ELSE @curRow := 1
				AND @curType := b.activity_id END) AS rank
		FROM
			(SELECT song_id,
					p.topic_id,
					p.activity_id,
					suggest
			FROM he_activity_match_songs p
			JOIN he_activity a ON (a.activity_id = p.activity_id
									AND a.match_no = p.match_no
									AND suggest = 1
									AND a.status = 1
									AND a.match_no > 0)
			ORDER BY p.activity_id) b ,
			(SELECT @curRow := 0, @curType := 0) r

		

		'''

	record = self.db.getAll(sql)
	dict = {}
        if record !=False:
            for r in record:
                topicid = r['topic_id']
                actid = r['activity_id']
                songid = r['song_id']
                key = str(topicid) + '_' + str(actid)
                if dict.has_key(key):
                        dict[key].append(songid)
                else:
                        dict[key] = [songid]



        return dict

    def getVuserid(self):
	sql = 'SELECT user_id FROM he_users WHERE user_level  =  1 '
	record = self.db.getAll(sql)
        return record
    

    def getActivityTime(self):
	sql = 'select  activity_id , start_time,end_time from he_activity '
	record = self.db.getAll(sql)
        return record


    def getPromotionSong(self):
	sql = 'SELECT activity_id , song_id ,order_no, visible_rank_score   from he_activity_match_songs where promotion = 1  '
        record = self.db.getAll(sql)
        return record


    #获取参赛的歌曲的信息    
    def getActSongInfo(self):
	sql = 'select s.id,a.topic_id,id,a.activity_id,song_id ,suggest,listen_num,visible_vote_num,visible_listen_num,visible_thumb_num,promotion from he_activity_match_songs s join he_activity a on (a.match_no = s.match_no and a.activity_id = s.activity_id) and s.match_no > 0 and a.status = 1 '
	record = self.db.getAll(sql)
	dict = {}
	if record != False:
	    for r in record:
		topicid = r['topic_id']
		actid = r['activity_id']
		songid = r['song_id']
		ms = matchsong.MatchSong(r['id'],actid,songid,r['promotion'],r['suggest'],r['listen_num'])
		#print '================',ms.id , ms.actid,ms.songid , ms.promotion
		dict[str(topicid)+','+str(actid)+','+str(songid)]=ms	
	
        return dict

    def updateSongInfo(self,actid,matchsong):
    	sql = 'update he_activity_match_songs set listen_num = %s,rank_score = %s,order_no = %s,visible_listen_num=%s,visible_vote_num=%s,visible_thumb_num = %s,visible_rank_score =%s,visible_vote_score =%s,visible_listen_score =%s,visible_collect_score =%s,visible_quantity_1 = %s,visible_quantity_2 = %s,visible_quantity_3 = %s,visible_quantity_4 = %s,visible_quantity_5 = %s,visible_quantity_6 = %s,visible_score_1 = %s,visible_score_2 = %s,visible_score_3 = %s,visible_score_4 = %s,visible_score_5 = %s,visible_score_6 = %s where song_id = %s and activity_id = %s  '
    	return self.db.update(sql,(matchsong.listen,matchsong.score,matchsong.order_no,matchsong.visible_listen_num,matchsong.visible_vote_num,matchsong.visible_thumb_num,matchsong.visible_rank_score ,matchsong.visible_vote_score,matchsong.visible_listen_score,matchsong.visible_collect_score,matchsong.visible_quantity_1,matchsong.visible_quantity_2,matchsong.visible_quantity_3,matchsong.visible_quantity_4,matchsong.visible_quantity_5,matchsong.visible_quantity_6,matchsong.visible_score_1,matchsong.visible_score_2,matchsong.visible_score_3,matchsong.visible_score_4,matchsong.visible_score_5,matchsong.visible_score_6 ,matchsong.songid,actid))


    #def updateSongInfo(self,matchsong):
    #    sql = 'update he_activity_match_songs set listen_num = %s,rank_score = %s,order_no = %s,visible_listen_num=%s,visible_vote_num=%s,visible_thumb_num = %s,visible_rank_score =%s where song_id = %s   '
    #    return self.db.update(sql,(matchsong.listen,matchsong.score,matchsong.order_no,matchsong.visible_listen_num,matchsong.visible_vote_num,matchsong.visible_thumb_num,matchsong.visible_rank_score ,matchsong.songid))

	
    def getPromotionSongs(self):
	sql = ' select activity_id,song_id  from he_activity_match_songs where  promotion = 1 '
	record = self.db.getAll(sql)
        return record

    def getActLimitSong(self):
	dict = {}
	sql = 'select m.activity_id ,song_limit_num from  he_activity_match m join he_activity a on m.activity_id = a.activity_id where m.match_no = a.match_no + 1 and a.match_no = 1 and a.status = 1'
	record = self.db.getAll(sql)
	if record != False:
     	    for r in record:
		dict[str(r['activity_id'])] = r['song_limit_num']	
        return dict
    def getDefaultSongInfos(self):
	dict = {}
	sql = 'select s.activity_id,s.song_id from  he_activity_match_songs s join he_activity a on s.activity_id = a.activity_id and s.match_no  = a.match_no and a.status = 1 '
	record = self.db.getAll(sql)
	for r in record:
	    actid = r['activity_id']
	    songid = r['song_id']
            if dict.has_key(actid):
		dict[actid].append(songid)
	    else:
		dict[actid]=[songid]
	return dict
#将数组等分成N块
    def chunks(arr, n):
    	return [arr[i:i+n] for i in range(0, len(arr), n)]

    def selectRatio(self):
	dict = {}
        sql = 'select a.activity_id,listen_ratio,fav_ratio,vote_ratio,quantity_1_ratio,quantity_2_ratio,quantity_3_ratio,quantity_4_ratio,quantity_5_ratio,quantity_6_ratio from  he_activity_match m join he_activity a on m.activity_id = a.activity_id where m.match_no = a.match_no'
	record = self.db.getAll(sql)
	if record is not None:
		for r in record:
		    actdict = {}
		    actdict['listen_ratio'] = r['listen_ratio'] 	
		    actdict['fav_ratio'] = r['fav_ratio']
		    actdict['vote_ratio'] = r['vote_ratio']
		    actdict['quantity_1_ratio'] = r['quantity_1_ratio']
		    actdict['quantity_2_ratio'] = r['quantity_2_ratio']
		    actdict['quantity_3_ratio'] = r['quantity_3_ratio']
		    actdict['quantity_4_ratio'] = r['quantity_4_ratio']
		    actdict['quantity_5_ratio'] = r['quantity_5_ratio']
		    actdict['quantity_6_ratio'] = r['quantity_6_ratio']
		    dict[str(r['activity_id'])] = actdict 
	logging.info('get all activity ratio ,the info is %s',dict)
	return dict

    def getTaskInfo(self):
	sql = 'select task_id,activity_id,task_type,content,status from  he_tasks where status  = 0'
	record = self.db.getAll(sql) 
	return record


    def updateTaskStatus(self,taskid):
	sql = 'update he_tasks set status = 1 where task_id = %s'
	param = (str(taskid),)
	return self.db.update(sql,param)
 	
 
    #获取下线的歌曲
    def getOfflineSong(self):
	sql = 'select activity_id,song_id from he_songs_info where check_status = -1'
	record = self.db.getAll(sql)
	dict = {}
        for r in record:
            actid = str(r['activity_id'])
            songid = r['song_id']
            if dict.has_key(actid):
                dict[actid].append(songid)
            else:
                dict[actid]=[songid]
        return dict

	#获取当前正在进行的活动
    def getAct(self):
	sql = 'select activity_id  from he_activity where status = 1'
	record = self.db.getAll(sql)
	actids = []
	if record !=False:
		for i in record:
			actids.append(i['activity_id'])
        return actids
	
