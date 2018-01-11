#!/usr/bin/python
# -*- coding: UTF-8 -*-
import httplib2
import urlparse
import urllib
import json
import urllib2


def getUrlContent(url):
    #h = httplib2.Http(".cache")
    try:
        print url
        http = httplib2.Http(".cache")
        resp, content = http.request(url, "GET")
    except  Exception,e:
        print e
        return {}
    #print content
    if 200 == resp.status:
        response = json.loads(content)
        return response
    return False

def postUrlContent(url,bodydata):
    print url
    h = httplib2.Http()
    headers={'Content-Type': 'application/x-www-form-urlencoded'}
    resp, content = h.request(url, "POST",body=urllib.urlencode(bodydata), headers=headers)
    print content
    if 200 == resp.status:
        response = json.loads(content)
        return response
    return False


def url2Dict(url):
    query = urlparse.urlparse(url).query
    return dict([(k, v[0]) for k, v in urlparse.parse_qs(query).items()])


def proxyGetContent(url):
    # 构建了两个代理Handler，一个有代理IP，一个没有代理IP
    print "proxy----"+url
    try:
        httpproxy_handler = urllib2.ProxyHandler({"http" : "112.114.93.31:8118"})
        nullproxy_handler = urllib2.ProxyHandler({})
        #定义一个代理开关
        proxySwitch = True
        # 通过 urllib2.build_opener()方法使用这些代理Handler对象，创建自定义opener对象
        # 根据代理开关是否打开，使用不同的代理模式
        if proxySwitch:
            opener = urllib2.build_opener(httpproxy_handler)
        else:
            opener = urllib2.build_opener(nullproxy_handler)

        request = urllib2.Request(url)

        # 使用opener.open()方法发送请求才使用自定义的代理，而urlopen()则不使用自定义代理。
        response = opener.open(request)

        # 就是将opener应用到全局，之后所有的，不管是opener.open()还是urlopen() 发送请求，都将使用自定义代理。
        # urllib2.install_opener(opener)
        # response = urlopen(request)

        content = response.read()
        print content
        response = json.loads(content)
        return response
    except urllib2.HTTPError, e:
        print e
        return False
