#!/usr/bin/python
# -*- coding: UTF-8 -*-
import sys
import os
import random
import time
reload(sys)
sys.setdefaultencoding('utf8')
WORK_NODE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# print CURRENT_DIR
WORK_NODE_DIR = os.path.dirname(WORK_NODE_DIR)
os.sys.path.insert(0, WORK_NODE_DIR)


from deps.lib.config import config
from deps.lib import redislib
import json
import urllib
from fans.lib import tool
from fans.lib.sinaWeibo import Weibo

#data为body数据，uid为加为哪个uid

userinfo_key = "user:info" #hash
user_province = "user:province" #zset
user_city = "user:city" #zset
user_verified = "user:verified" #zset
user_verified_type = "user:verified:type" #zset
userinfo_has = "user:info:had" #set
user_followers_count = "user:followers:count"
user_friends_count = "user:friends:count"
user_statuses_count = "user:statuses:count"
user_favourites_count = "user:favourites:count"
user_created_at = "user:created:at"
user_gender = "user:gender"
user_level = "user:level"
user_type = "user:type"
user_class = "user:class"
user_ulevel = "user:ulevel"
user_mbtype = "user:mbtype"
user_mbrank = "user:mbrank"
user_id = "user_id"
user_followers = "user:follow:"#粉丝列表
user_friend = "user:friend:" #关注列表



weibo_obj = Weibo()

def saveUserInfo(redisObj,item,fan_des_uid=0,follow_des_uid=0):#谁的粉丝，谁的关注
    global weibo_obj
    has_info = redisObj.sismember(userinfo_has,item["user"]["id"])
    print has_info
    if has_info:
        return True
    seconds = random.randint(1,3)
    time.sleep(seconds)
    profile_para = {}
    userinfo = weibo_obj.person_userInfo(profile_para,item["user"]["id"])
    if userinfo:
        if ("用户" in userinfo["screen_name"]) and (0 == userinfo["statuses_count"]):
            return False
        if not userinfo["verified_type"]:
            userinfo["verified_type"] = -1
        if not userinfo["followers_count"]:
            userinfo["followers_count"] = 0
        if not userinfo["friends_count"]:
            userinfo["friends_count"] = 0
        if not userinfo["statuses_count"]:
            userinfo["statuses_count"] = 0
        if not userinfo["favourites_count"]:
            userinfo["favourites_count"] = 0
        if not userinfo["created_at"]:
            userinfo["created_at"] = time.ctime()
        if not userinfo["gender"]:
            userinfo["gender"] = ""
        if not userinfo["level"]:
            userinfo["level"] = -1
        if not userinfo["mbtype"]:
            userinfo["mbtype"] = 0
        if not userinfo["mbrank"]:
            userinfo["mbrank"] = 0
        if not userinfo["type"]:
            userinfo["type"] = -1


        userid = userinfo['id']
        redisObj.sadd(userinfo_has,userid)
        redisObj.hset(userinfo_key,userid,json.dumps(userinfo))
        redisObj.zadd(user_province,userid,userinfo["province"])
        redisObj.zadd(user_city,userid,userinfo["city"])
        fan_des_uid = str(fan_des_uid)
        if fan_des_uid:
            redisObj.sadd(user_followers+fan_des_uid,userid)
        if follow_des_uid:
            redisObj.sadd(user_friend+follow_des_uid,userid)
        verified = 0
        if userinfo["verified"]:
            verified = 1
        else:
            verified = 0
        redisObj.zadd(user_verified,userid,verified)
        redisObj.zadd(user_verified_type,userid,userinfo["verified_type"])
        redisObj.zadd(user_followers_count,userid,userinfo["followers_count"])
        redisObj.zadd(user_friends_count,userid,userinfo["friends_count"])
        redisObj.zadd(user_statuses_count,userid,userinfo["statuses_count"])
        redisObj.zadd(user_favourites_count,userid,userinfo["favourites_count"])
        create_at = userinfo["created_at"]
        create_at = create_at.replace(" +0800 "," ")
        create_at = time.mktime(time.strptime(create_at, '%a %b %d %H:%M:%S %Y'))
        redisObj.zadd(user_created_at,userid,create_at)
        gender = 0
        if "m" == userinfo["gender"]:
            gender=1
        elif "f" == userinfo["gender"]:
            gender = 2
        redisObj.zadd(user_gender,userid,gender)
        redisObj.zadd(user_level,userid,userinfo["level"])
        redisObj.zadd(user_type,userid,userinfo["type"])
        redisObj.zadd(user_mbtype,userid,userinfo["mbtype"])
        redisObj.zadd(user_mbrank,userid,userinfo["mbrank"])
        redisObj.zadd(user_id,userid,userid)



def searchUser(src_uid = "2835724503"):

    global weibo_obj
    redis = redislib.RedisTools()
    redisObj = redis.get_redis()

    #基本思路，从某人粉丝列表中，拉取用户信息存储必要信息，并区分用户类型

    since_id=1
    weibo_obj.fans_since_id = since_id
    while (True):
        fans_para = {}
        fans_list = weibo_obj.person_fans(fans_para,src_uid)
        if fans_list:
            for item in fans_list:
                if "userinfo" in item["scheme"]:
                    saveUserInfo(redisObj,item,src_uid)
        else:
            break

    while(True):
        follower_para = {}
        follwer_list = weibo_obj.person_follow(follower_para,src_uid)
        print follwer_list
        if follwer_list:
            for follower_item in follwer_list:
                item_id = follower_item["user"]["id"]
                redisObj.sadd(user_friend+src_uid,item_id)
                fans_para = {}
                weibo_obj.fans_since_id = 0
                weibo_obj.fans_page = 0
                fans_list = weibo_obj.person_fans(fans_para,item_id)
                if fans_list:
                    for item in fans_list:
                        if "userinfo" in item["scheme"]:
                            saveUserInfo(redisObj,item,item_id)
        else:
            break

    redisObj.disconnect()


def sendMsgToAll(text_arr):
        global weibo_obj
        msgindex = "1"
        redis = redislib.RedisTools()
        redisObj = redis.get_redis()
        str = ','.join(text_arr)
        redisObj.delete("msg:"+str)
        index = 0
        param=[{"text":"","gsid":"_2A253QhvhDeRxGeBK6loX-CvPzjyIHXVSVigprDV6PUJbkdANLXT6kWpNR8iRakJk0MsW2ydDL3e-mPsy61wijpuN","c":"android","s":"a26842eb"},
               {"text":"","gsid":"_2A253Tiu_DeTxGeBK6FUZ8CbOyTiIHXVSWjh3rDV6PUJbi9ANLRDjkWpNR6uX1DmujTwilh1znszrjjb1-ulqR13p","c":"android","s":"f8367093"},
               {"text":"","gsid":"_2AkMtF9sLf8NhqwJRmPERxGjlbY5xzwDEieKbSyrQJRMxHRl-wT9jqn0ItRV6Bpf1yKtXKLSpBsWMIhSSoZH4a_UnveOO","c":"android","s":"2e844781"},
               {"text":"","gsid":"_2AkMtFiRWf8NhqwJRmPEWxGPra4h3zQ7EieKbStWNJRMxHRl-wT9kqm0htRV6Bu124lTCBA5LPZ__HkNmxbbLulOE_5mU","c":"android","s":"e7111929"},
               {"text":"","gsid":"_2A253QyRGDeRxGeNG61sZ8C3JwjiIHXVSWTCOrDV6PUJbkdANLRffkWpNS5Ur8Rl21xhCn7AaQTDvR5RYVuLSE55-","c":"android","s":"7d5f5fa8"},
               {"text":"","gsid":"_2AkMtF8Dif8NhqwJRmPAXy2nmb4RwzwvEieKbSzE5JRMxHRl-wT9kqkIbtRV6BZdIWKAWH8yeHWLrObLuwGm_mG5mVpql","c":"android","s":"1e85a870"},
               {"text":"","gsid":"_2AkMtF9zqf8NhqwJRmPERxGjlbIt-zQHEieKbSy0xJRMxHRl-wT9kqm9atRV6BpfyBYcdgoD9veV_bMEvToqyirtZb8zo","c":"android","s":"67eec36b"},
               {"text":"","gsid":"_2A253TyNLDeTxGeBK71sQ9S7JzzSIHXVSXTGDrDV6PUJbltAKLXT-kWpNR6KobQVKnLQZXbmnEYYIPAO9z0t1ilbx","c":"android","s":"23fe3f69"},
               {"text":"","gsid":"_2A253TyBXDeRxGeBK6FYW8SnPwz-IHXVSXTSfrDV6PUJbkdAKLXXakWpNR9jcqE936fHteT80n5vubgvsXluBrN98","c":"android","s":"2a925eb0"},
               {"text":"","gsid":"_2AkMtF9t2f8NhqwJRmPAWz2rmaYR2yg_EieKbSyqtJRMxHRl-wT9kqmIStRV6BZN_2HH4MfeAozmyMKJKm2VPphIGwD1f","c":"android","s":"7f83ecf1"},
               ]
        while True:
            uid_arr = redisObj.zrange(user_id,index,index+10)
            print uid_arr
            index += 10
            if uid_arr:
                for uid in uid_arr:
                    if not param:
                        sys.exit(0)
                    has_send = redisObj.sismember("msg:"+msgindex,uid)
                    verified_type = redisObj.zscore(user_verified_type,uid)

                    if not verified_type:
                        verified_type = -1
                    verified_type = int(verified_type)
                    if has_send or -1 < verified_type:
                        continue
                    print uid
                    seconds = random.randint(40,50)
                    time.sleep(seconds)
                    send = False
                    for text in text_arr:
                        index = random.randint(0,len(param)-1)
                        print index
                        param[index]["text"]=text
                        send = weibo_obj.send_msg(param[index],uid)
                        time.sleep(5)
                    if send:
                        redisObj.sadd("msg:"+msgindex,uid)
                    else:
                        del param[index]
            else:
                break

if __name__ == '__main__':

    operate_type = sys.argv[1]
    operate_param  = sys.argv[2:]
    if "getuser":#更新用户，uid跟
        if operate_param:
            for v in operate_param:
                if v.isdigit():
                    searchUser(v)
        else:
            searchUser()
    if "sendmsg" == operate_type:
        if "all" == operate_param[0]:
            #text_param  = sys.argv[3:]
            #for v in text_param:
            sendMsgToAll(['''
                淘宝购买，返现金
                
                我使用返利很久了，送个红包给你，邀请你一起来！
                
                
http://1514964178.wx.fanli.com/come?id=105306985&spm=fl_invite_reg.h5.pty-open~std-30326&t=11


来自:返利网''',"http://1514964178.wx.fanli.com/come?id=105306985&spm=fl_invite_reg.h5.pty-open~std-30326&t=11"])
    file = config['log_path']
    '''
    fo = open(file,"r")
    while True:
        line = fo.readline()
        if ("" == line):
            break
        dataArr = line.split(',')
        print dataArr[8]
        break
    fo.close()
'''


