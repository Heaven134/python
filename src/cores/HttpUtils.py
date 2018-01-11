# /usr/env python
# -*- coding: UTF-8 -*-

import os    

WORK_NODE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# print CURRENT_DIR
os.sys.path.insert(0, os.path.dirname(WORK_NODE_DIR))
import httplib
from src.conf import config
from src.cores import my_logger as logging


responseDict = {}

class HttpUtils():
  
    def __init__(self):
	apiconf = config['apiconf']
	self.host = apiconf['host']
	self.port = apiconf['port']

    #split list
    def split_list(lst):
	return [lst[i:i+3] for i in xrange(0,len(lst),3)]



    def getActsong(self,type,actid,songid):
       host = self.host
       port = self.port
       url = '/vote/themetotal/getnum?pid=heyinliang&tid='+type+'&actid='+str(actid)+'&orderby=hot&desc=1&start=0&itemid='+str(songid)
       httpClient = None

       try:
           httpClient = httplib.HTTPConnection(host, port, timeout=30)
           httpClient.request('GET', url)

           #logging.info('the request is %s','http://'+host+':'+port+url)
           #response是HTTPResponse对象
           response = httpClient.getresponse()
           res = response.read()
           logging.info('the request is %s and the response info is %s','http://'+host+':'+port+url,res)
	   return res
       except Exception, e:
           logging.error('http request error,the error info is %s',e)
       finally:
           if httpClient:
               httpClient.close()



    #指定活动下的所有项（或者某些项的）的点赞、收藏、投票结果总数
    def getHttpReq(self,type,actid):


        if responseDict.has_key(str(actid)+','+type):
                return responseDict[str(actid)+','+type]
        else:
                host = self.host
                port = self.port
                url = '/vote/themetotal/getnum?pid=heyinliang&tid='+type+'&actid='+str(actid)+'&orderby=hot&desc=1&start=0'
                httpClient = None

                try:
                    httpClient = httplib.HTTPConnection(host, port, timeout=30)
                    httpClient.request('GET', url)

                    #logging.info('the request is %s','http://'+host+':'+port+url)
                    #response是HTTPResponse对象
                    response = httpClient.getresponse()
                    res = response.read()
                    logging.info('the request is %s and the response info is %s','http://'+host+':'+port+url,res)
                    responseDict[str(actid)+','+type] = res
                except Exception, e:
		    logging.error('http request error,the error info is %s',e)
                finally:
                    if httpClient:
                        httpClient.close()

                if responseDict.has_key(str(actid)+','+type):
                        return responseDict[str(actid)+','+type]
                else:
                        return ''
    def getHttpReqByUser(self,type,actid,userids):
	

         host = self.host
         port = self.port
         print '------------host---',host
	 url = '/vote/theme/getsets?pid=heyinliang&tid='+type+'&actid='+str(actid)+'&orderby=hot&desc=1&start=0&userid='+userids
         httpClient = None
    
         try:
             httpClient = httplib.HTTPConnection(host, port, timeout=30)
             httpClient.request('GET', url)

             #logging.info('the request is %s','http://'+host+':'+port+url)
             #response是HTTPResponse对象
             response = httpClient.getresponse()
             res = response.read()
             logging.info('the request is %s and the response info is %s','http://'+host+':'+port+url,res)
             return res
         except Exception, e:
             print e
         finally:
             if httpClient:
                 httpClient.close()

