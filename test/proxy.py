#!/usr/bin/python
# -*- coding: UTF-8 -*-

import urllib2

# 构建了两个代理Handler，一个有代理IP，一个没有代理IP
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

request = urllib2.Request("https://api.weibo.cn/2/cardlist?gsid=_2A253QKqkDeRxGedG7FUV9SrEzj-IHXVSe4yrrDV6PUJbkdANLVOkkWpNURhDX4-J0g56Z9EaUoTXjQYW8H5b7gFC&wm=3333_2001&i=9b17ad6&b=0&from=107C293010&c=iphone&networktype=wifi&v_p=56&skin=default&v_f=1&s=56f20f9b&lang=zh_CN&sflag=1&ua=iPhone9,1__weibo__7.12.2__iphone__os11.1&ft=0&aid=01Av9tn9LLqR5apU_SfKnDUAMVv9vfJMkky4Iji-ZgVaGL9mc.&moduleID=pagecard&uicode=10000011&featurecode=10000001&feed_mypage_card_remould_enable=1&luicode=10000198&count=50&containerid=231051_-_fans_-_5685358568&fid=231051_-_fans_-_5685358568&lfid=2302835685358568&page=1&need_head_cards=0")

# 使用opener.open()方法发送请求才使用自定义的代理，而urlopen()则不使用自定义代理。
response = opener.open(request)

# 就是将opener应用到全局，之后所有的，不管是opener.open()还是urlopen() 发送请求，都将使用自定义代理。
# urllib2.install_opener(opener)
# response = urlopen(request)

print response.read()