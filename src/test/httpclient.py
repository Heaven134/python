#!/usr/bin/env python
#coding=utf8

import httplib
 
httpClient = None
 
try:
    httpClient = httplib.HTTPConnection('192.168.217.11', 8258, timeout=30)
    httpClient.request('GET', '/themetotal/getnum?pid=heyinliang&tid=thumb&actid=102&orderby=hot&desc=1&start=0')
 
    #response是HTTPResponse对象
    response = httpClient.getresponse()
    print response.status
    print response.reason
    print response.read()
except Exception, e:
    print e
finally:
    if httpClient:
        httpClient.close()
