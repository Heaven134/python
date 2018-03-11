#!/usr/bin/python
# -*- coding: UTF-8 -*-
from fans.lib import tool
import types
import urllib
import re
import sys
from random import choice

class Weibo:
    __profile_url = "https://api.weibo.cn/2/profile?gsid=_2A253O_hADeRxGeBK71AX8y7IyTqIHXVSUQyIrDV6PUJbkdANLWXMkWpNR9QQdnUVOnhh0FUN9YhQKBeQmuSQfF9I&wm=90113_90001&i=61b977d&from=257C095010&c=android&s=3843602f&lang=zh_CN&ua=HUAWEI-G620-L75__weibo_lightning__1.0.9__android__android4.3&aid=01Ah8Ah2M5nZRK8BtKqdsa1RvwuufRgiBxG3zOh1E8Xm03ttM.&uicode=10000617&luicode=10000617&fid=userinfo&lfid=detail&uid=1854283601&imei=864085029799976&appkey=7501641714&device_id=dd9ada681c33d71bf5e0faccf8056e670148a789&l_v=5"
    __fans_url = "https://api.weibo.cn/2/cardlist?gsid=_2A253O_hADeRxGeBK71AX8y7IyTqIHXVSUQyIrDV6PUJbkdANLWXMkWpNR9QQdnUVOnhh0FUN9YhQKBeQmuSQfF9I&wm=90113_90001&i=61b977d&from=257C095010&c=android&s=3843602f&lang=zh_CN&ua=HUAWEI-G620-L75__weibo_lightning__1.0.9__android__android4.3&aid=01Ah8Ah2M5nZRK8BtKqdsa1RvwuufRgiBxG3zOh1E8Xm03ttM.&uicode=10000617&luicode=10000617&containerid=231051_-_fans_-_1854283601&fid=userinfo&lfid=detail&page=1&need_head_cards=0&uid=1854283601&imei=864085029799976&appkey=7501641714&device_id=dd9ada681c33d71bf5e0faccf8056e670148a789&l_v=5&fid=231051_-_fans_-_1854283601"
    __follower_url = "https://api.weibo.cn/2/cardlist?gsid=_2A253QKqkDeRxGedG7FUV9SrEzj-IHXVSe4yrrDV6PUJbkdANLVOkkWpNURhDX4-J0g56Z9EaUoTXjQYW8H5b7gFC&wm=3333_2001&i=9b17ad6&b=0&from=107C293010&c=iphone&networktype=wifi&v_p=56&skin=default&v_f=1&s=56f20f9b&lang=zh_CN&sflag=1&ua=iPhone9,1__weibo__7.12.2__iphone__os11.1&ft=0&aid=01Av9tn9LLqR5apU_SfKnDUAMVv9vfJMkky4Iji-ZgVaGL9mc.&moduleID=pagecard&uicode=10000011&featurecode=10000085&feed_mypage_card_remould_enable=1&luicode=10000198&count=20&containerid=231051_-_followers_-_1854283601&fid=231051_-_followers_-_1854283601&lfid=2302831854283601&page=1&need_head_cards=0"

    __send_msg = {}
    __send_msg["aid"] = "01Alz_2_iNNX3f1CXhVgiX2mHxkYyhdCfGysl_947nkM505rc."
    __send_msg["from"] = "1228493010"
    __send_msg["i"] = "9b17ad6"
    __send_msg["lang"] = "zh_CN"
    __send_msg["ua"] = "iPhone9,1__weibo__7.12.2__iphone__os11.1"
    __send_msg["v_p"] = "50"
    def __init__(self):
        self.fans_since_id = 0
        self.follow_page = 1


    def rand_url(self):

        userparam = []
        one={"c":"android","s":"fcd0645f","gsid":"_2AkMtatk2f8NhqwJRmPASz23iaIVzww3EieKbNijtJRMxHRl-wT9kqk4YtRV6BU1o2IcTjb_bfaESNSDatf_OBLF1xjo3"}
        userparam.append(one)
        one={"c":"android","s":"8ca67ace","gsid":"_2A253QfCtDeRxGedJ7FAQ-SjJwzyIHXVSVwNlrDV6PUJbkdANLWHMkWpNUaSvqxX6pMxd8FdJzUhqBPqUC91gC1E1"}
        userparam.append(one)
        one={"c":"android","s":"cbced773","gsid":"_2A253TMgcDeRxGeBO7lcT8SjKwj-IHXVSWFzUrDV6PUJbkdANLW7TkWpNRfjsg3v3NKn8EiNdHMFFSwZl4d933EDp"}
        userparam.append(one)
        one={"c":"android","s":"5f2a2aa9","gsid":"_2A253TNVhDeTxGeBK71MZ8y7Eyz2IHXVSWG-prDV6PUJbltANLUrYkWpNR6PBf1_s_Fo2ded1NptsnRBRFL1asUVC"}
        userparam.append(one)
        one={"c":"android","s":"1cf8ec5b","gsid":"_2A253MIcVDeRxGeBK61MY8ibJzjiIHXVVn-a9rDV6PUJbmdANLUzDkWpNHetkT3EbyFQ4MdLlxibrhQtXKR6i9_XY"}
        userparam.append(one)
        one={"c":"android","s":"0a3d6e77","gsid":"_2AkMtF9zdf8NhqwJRmPERxGjlbIp-ywnEieKbSy0GJRMxHRl-wT9kqkUatRV6BpfyMrhdWXocCZXjmELjqcsqz9ThVjZu"}
        userparam.append(one)
        one={"c":"android","s":"f646a81b","gsid":"_2A253TTzHDeTxGeBK71QU8ibOzzWIHXVSWzcPrDV6PUJbltANLWKlkWpNR66h11mXGcTTUPSSUIQiFa6gJlwhh229"}
        userparam.append(one)
        one={"c":"android","s":"e4827bf5","gsid":"_2A253T2gzDeRxGeNO71sT-CbJyD2IHXVSXfz7rDV6PUJbkdAKLWihkWpNTuAmaT4pqXuykY9dD7rSKPz5yKSYG3c2"}
        userparam.append(one)
        one={"c":"android","s":"5ff555fa","gsid":"_2A253MgJ1DeRxGeRK7VIS9SfOyz2IHXVSZhK9rDV6PUJbkdANLWLCkWpNU1aTGDUohCphpRwqiiVHO8cAOGlfEFyU"}
        userparam.append(one)
        one={"c":"android","s":"ca0cd4b5","gsid":"_2A253T3--DeRxGeNG6lYS9izJyDuIHXVSXfR2rDV6PUJbkdANLVfCkWpNS23jbnNuhEQZTEP8bBPVhpcB2-9tmLM0"}
        userparam.append(one)
        one={"c":"android","s":"dc7fee4a","gsid":"_2A253TlCHDeRxGeBN6lES9SbOwz-IHXVSWuNPrDV6PUJbkdANLRfxkWpNRIqOtiOaa0-tKgTx5Ly1EnLDgCylG2oQ"}
        userparam.append(one)
        one_param = choice(userparam)

        gsid=one_param["gsid"]
        c = one_param["c"]
        s = one_param["s"]
        self.__profile_url,num = re.subn("gsid=(.*?)&",'gsid='+gsid+'&', self.__profile_url)
        self.__profile_url,num = re.subn("&c=(.*?)&",'&c='+c+'&', self.__profile_url)
        self.__profile_url,num = re.subn("&s=(.*?)&",'&s='+s+'&', self.__profile_url)
        self.__fans_url,num = re.subn("gsid=(.*?)&",'gsid='+gsid+'&', self.__fans_url)
        self.__fans_url,num = re.subn("&c=(.*?)&",'&c='+c+'&', self.__fans_url)
        self.__fans_url,num = re.subn("&s=(.*?)&",'&s='+s+'&', self.__fans_url)
        self.__follower_url,num = re.subn("gsid=(.*?)&",'gsid='+gsid+'&', self.__follower_url)
        self.__follower_url,num = re.subn("&c=(.*?)&",'&c='+c+'&', self.__follower_url)
        self.__follower_url,num = re.subn("&s=(.*?)&",'&s='+s+'&', self.__follower_url)

        #发送消息
        self.__send_msg["gsid"] = gsid
        self.__send_msg["c"] = c
        self.__send_msg["s"] = s
    #获取某用户的粉丝列表
    def person_fans(self,url_param,uid):
        uid = str(uid)
        if type(url_param) is not types.DictType:
            if type(url_param) is types.StringType:
                url_param = tool.url2Dict(url_param)
            else:
                return {}
        self.rand_url()
        fans_para = tool.url2Dict(self.__fans_url)
        fans_para["since_id"] = self.fans_since_id
        for param_k,param_v in url_param.items():
            fans_para[param_k] = param_v
        fans_para["uid"] = uid
        fans_para['containerid']="231051_-_fans_-_"+uid
        fans_para["fid"] = "231051_-_fans_-_"+uid
        fans_para["lfid"] = "230283"+uid
        fans_url = "https://api.weibo.cn/2/cardlist?" + urllib.urlencode(fans_para)
        print self.fans_since_id
        fans_list = tool.getUrlContent(fans_url)
        if fans_list:
            try:

                self.fans_since_id = fans_list["cardlistInfo"]["since_id"]
                cards = fans_list["cards"][len(fans_list["cards"])-1]
                card_group = cards["card_group"]
                return card_group
            except Exception,e:
                return {}
        return {}

    #获取用户信息
    def person_userInfo(self,url_param,uid):
        '''
        self.rand_url()
        userinfo_param = tool.url2Dict(self.__profile_url)
        for param_k,param_v in url_param.items():
            userinfo_param[param_k] = param_v
        userinfo_param["user_domain"] = uid
        profile_url = "https://api.weibo.cn/2/profile?" + urllib.urlencode(userinfo_param)
        '''
        uid = str(uid)
        profile_url = "https://api.weibo.cn/2/profile?user_domain="+str(uid)
        #profile = tool.proxyGetContent(profile_url)
        profile = tool.getUrlContent(profile_url)
        print uid
        if profile:
            try:
                userinfo = profile['userInfo']
                return userinfo

            except Exception,e:
                return {}
        else:
            return {}

    #获取用户的关注列表
    def person_follow(self,url_param,uid):
        print uid
        uid = str(uid)
        if type(url_param) is not types.DictType:
            if type(url_param) is types.StringType:
                url_param = tool.url2Dict(url_param)
            else:
                return {}
        self.rand_url()
        fans_para = tool.url2Dict(self.__fans_url)
        for param_k,param_v in url_param.items():
            fans_para[param_k] = param_v
        fans_para["uid"] = uid
        fans_para["page"] = self.follow_page
        fans_para['containerid']="231051_-_followers_-_"+uid
        fans_para["fid"] = "231051_-_followers_-_"+uid
        fans_para["lfid"] = "230283"+uid
        fans_url = "https://api.weibo.cn/2/cardlist?" + urllib.urlencode(fans_para)
        fans_list = tool.getUrlContent(fans_url)
        self.follow_page += 1
        if fans_list:
            try:
                cards = fans_list["cards"][len(fans_list["cards"])-1]
                card_group = cards["card_group"]
                return card_group
            except Exception,e:
                return {}
        return {}

    #给用户发私信
    def send_msg(self,url_param,uid):
        uid = str(uid)
        self.rand_url()
        if type(url_param) is not types.DictType:
            return False
        for param_k,param_v in url_param.items():
            self.__send_msg[param_k] = param_v
        self.__send_msg["uid"] = uid
        sendresult = tool.postUrlContent("https://api.weibo.cn/2/direct_messages/create",self.__send_msg)
        if sendresult.has_key("errno"):
            return False
        return True

    #浏览某用户
    def person_browse(self,url_param,uid):
        uid = str(uid)
        if type(url_param) is not types.DictType:
            if type(url_param) is types.StringType:
                url_param = tool.url2Dict(url_param)
            else:
                return {}
        cururl_para = tool.url2Dict("https://api.weibo.cn/2/stories/exist?gsid=_2A253UqW1DeRxGeBK61QW8i_EzzuIHXVSSb59rDV6PUJbkdANLRHwkWpNR_4pDT5xGeh3D3L_tq3fphqWEtcPPV_8&wm=3333_2001&i=9b17ad6&b=0&from=107C293010&c=iphone&networktype=wifi&v_p=56&skin=default&v_f=1&s=3c8f3a0a&lang=zh_CN&sflag=1&ua=iPhone9,1__weibo__7.12.2__iphone__os11.1&ft=0&aid=01Av9tn9LLqR5apU_SfKnDUAO9Wacfs76KIEBqPTg2v5UOHNk.&moduleID=pagecard&uicode=10000198&featurecode=10000001&id=6004281123&mid=4195012604100383&luicode=10000001&_status_id=4195012604100383&rid=0_0_8_3080955430742652852&fromlog=100016406721847&lfid=100016406721847")
        for param_k,param_v in url_param.items():
            cururl_para[param_k] = param_v
        cururl_para["uid"] = uid
        url = "https://api.weibo.cn/2/stories/exist?" + urllib.urlencode(cururl_para)
        url_content = tool.getUrlContent(url)

        sys.sleep(4)
        self.__person_profile(url_param,uid)
        sys.sleep(5)
        self.__person_unread_count(url_param,uid)
        sys.sleep(6)
        self.__person_cardlist(url_param,uid)
        sys.sleep(6)
        self.__person_clientchatpanel(url_param,uid)
        sys.sleep(8)
        self.__person_messmenu(url_param,uid)
        sys.sleep(2)
        self.__person_relation(url_param,uid)
        return
    #浏览某用户
    def person_relation(self,url_param,uid):
        uid = str(uid)
        if type(url_param) is not types.DictType:
            if type(url_param) is types.StringType:
                url_param = tool.url2Dict(url_param)
            else:
                return {}
        cururl_para = tool.url2Dict("https://api.weibo.cn/2/users/relation?gsid=_2A253UqW1DeRxGeBK61QW8i_EzzuIHXVSSb59rDV6PUJbkdANLRHwkWpNR_4pDT5xGeh3D3L_tq3fphqWEtcPPV_8&wm=3333_2001&i=9b17ad6&b=0&from=107C293010&c=iphone&networktype=wifi&v_p=56&skin=default&v_f=1&s=3c8f3a0a&lang=zh_CN&sflag=1&ua=iPhone9,1__weibo__7.12.2__iphone__os11.1&ft=0&aid=01Av9tn9LLqR5apU_SfKnDUAO9Wacfs76KIEBqPTg2v5UOHNk.&uicode=10000073&uid=6004281123&featurecode=10000001&luicode=10000198&fid=6004281123&lfid=1078036004281123&screen_name=%E6%A2%A8%E8%A7%86%E9%A2%91&has_block=1")
        for param_k,param_v in url_param.items():
            cururl_para[param_k] = param_v
        cururl_para["uid"] = uid
        cururl_para["fid"] = uid
        cururl_para["lfid"] = "107803"+uid
        url = "https://api.weibo.cn/2/users/relation?" + urllib.urlencode(cururl_para)
        url_content = tool.getUrlContent(url)

    #用户菜单

    def __person_messmenu(self,url_param,uid):
        uid = str(uid)
        if type(url_param) is not types.DictType:
            if type(url_param) is types.StringType:
                url_param = tool.url2Dict(url_param)
            else:
                return {}
        cururl_para = tool.url2Dict("https://api.weibo.cn/2/messages/menu_show?gsid=_2A253UqW1DeRxGeBK61QW8i_EzzuIHXVSSb59rDV6PUJbkdANLRHwkWpNR_4pDT5xGeh3D3L_tq3fphqWEtcPPV_8&wm=3333_2001&i=9b17ad6&b=0&from=107C293010&c=iphone&networktype=wifi&v_p=56&skin=default&v_f=1&s=3c8f3a0a&lang=zh_CN&sflag=1&ua=iPhone9,1__weibo__7.12.2__iphone__os11.1&ft=0&aid=01Av9tn9LLqR5apU_SfKnDUAO9Wacfs76KIEBqPTg2v5UOHNk.&uid=6004281123")
        for param_k,param_v in url_param.items():
            cururl_para[param_k] = param_v
        cururl_para["uid"] = uid
        url = "https://api.weibo.cn/2/messages/menu_show?" + urllib.urlencode(cururl_para)
        url_content = tool.getUrlContent(url)
        return url_content

    #用户聊天面版

    def __person_clientchatpanel(self,url_param,uid):
        uid = str(uid)
        if type(url_param) is not types.DictType:
            if type(url_param) is types.StringType:
                url_param = tool.url2Dict(url_param)
            else:
                return {}
        cururl_para = tool.url2Dict("https://api.weibo.cn/2/client/chatpanel?gsid=_2A253UqW1DeRxGeBK61QW8i_EzzuIHXVSSb59rDV6PUJbkdANLRHwkWpNR_4pDT5xGeh3D3L_tq3fphqWEtcPPV_8&wm=3333_2001&i=9b17ad6&b=0&from=107C293010&c=iphone&networktype=wifi&v_p=56&skin=default&v_f=1&s=3c8f3a0a&lang=zh_CN&sflag=1&ua=iPhone9,1__weibo__7.12.2__iphone__os11.1&ft=0&aid=01Av9tn9LLqR5apU_SfKnDUAO9Wacfs76KIEBqPTg2v5UOHNk.&")
        for param_k,param_v in url_param.items():
            cururl_para[param_k] = param_v
        url = "https://api.weibo.cn/2/client/chatpanel?" + urllib.urlencode(cururl_para)
        url_content = tool.getUrlContent(url)
        return url_content

    #用户cardlist

    def __person_cardlist(self,url_param,uid):
        uid = str(uid)
        if type(url_param) is not types.DictType:
            if type(url_param) is types.StringType:
                url_param = tool.url2Dict(url_param)
            else:
                return {}
        cururl_para = tool.url2Dict("https://api.weibo.cn/2/cardlist?gsid=_2A253UqW1DeRxGeBK61QW8i_EzzuIHXVSSb59rDV6PUJbkdANLRHwkWpNR_4pDT5xGeh3D3L_tq3fphqWEtcPPV_8&wm=3333_2001&i=9b17ad6&b=0&from=107C293010&c=iphone&networktype=wifi&v_p=56&skin=default&v_f=1&s=3c8f3a0a&lang=zh_CN&sflag=1&ua=iPhone9,1__weibo__7.12.2__iphone__os11.1&ft=0&aid=01Av9tn9LLqR5apU_SfKnDUAO9Wacfs76KIEBqPTg2v5UOHNk.&mid=4195012604100383&_status_id=4195012604100383&count=20&luicode=10000001&containerid=1078036004281123&featurecode=10000001&uicode=10000198&fid=1078036004281123&rid=0_0_8_3080955430742652852&fromlog=100016406721847&need_head_cards=0&page=1&lfid=100016406721847&moduleID=pagecard&since_id=4194771415644594_4194791794737655_20180111_-1")
        for param_k,param_v in url_param.items():
            cururl_para[param_k] = param_v
        cururl_para["containerid"] = "107803"+uid
        cururl_para["fid"] = "107803"+uid
        url = "https://api.weibo.cn/2/cardlist?" + urllib.urlencode(cururl_para)
        url_content = tool.getUrlContent(url)

        sys.sleep(2)
        cururl_para["containerid"] = "107803"+uid+"_-_mcn"
        cururl_para["fid"] = "107803"+uid+"_-_mcn"
        url = "https://api.weibo.cn/2/cardlist?" + urllib.urlencode(cururl_para)
        url_content = tool.getUrlContent(url)

        sys.sleep(2)
        cururl_para["containerid"] = "230283"+uid
        cururl_para["fid"] = "230283"+uid
        url = "https://api.weibo.cn/2/cardlist?" + urllib.urlencode(cururl_para)
        url_content = tool.getUrlContent(url)
        return url_content

    ###
    def __person_unread_count(self,url_param,uid):
        uid = str(uid)
        if type(url_param) is not types.DictType:
            if type(url_param) is types.StringType:
                url_param = tool.url2Dict(url_param)
            else:
                return {}
        cururl_para = tool.url2Dict("https://api.weibo.cn/2/remind/unread_count?wm=3333_2001&i=9b17ad6&b=0&from=107C293010&c=iphone&networktype=wifi&v_p=56&skin=default&v_f=1&lang=zh_CN&sflag=1&ua=iPhone9,1__weibo__7.12.2__iphone__os11.1&ft=0&aid=01Av9tn9LLqR5apU_SfKnDUAO9Wacfs76KIEBqPTg2v5UOHNk.&with_page_group=1&with_settings=1&s=3c8f3a0a&with_comment_attitude=1&gsid=_2A253UqW1DeRxGeBK61QW8i_EzzuIHXVSSb59rDV6PUJbkdANLRHwkWpNR_4pDT5xGeh3D3L_tq3fphqWEtcPPV_8&with_common_cmt=1")
        for param_k,param_v in url_param.items():
            cururl_para[param_k] = param_v
        url = "https://api.weibo.cn/2/remind/unread_count?" + urllib.urlencode(cururl_para)
        url_content = tool.getUrlContent(url)
        return url_content

    #get_item

    def __person_get_item(self,url_param,uid):
        uid = str(uid)
        if type(url_param) is not types.DictType:
            if type(url_param) is types.StringType:
                url_param = tool.url2Dict(url_param)
            else:
                return {}
        cururl_para = tool.url2Dict("https://api.weibo.cn/2/container/get_item?gsid=_2A253UqW1DeRxGeBK61QW8i_EzzuIHXVSSb59rDV6PUJbkdANLRHwkWpNR_4pDT5xGeh3D3L_tq3fphqWEtcPPV_8&wm=3333_2001&i=9b17ad6&b=0&from=107C293010&c=iphone&networktype=wifi&v_p=56&skin=default&v_f=1&s=3c8f3a0a&lang=zh_CN&sflag=1&ua=iPhone9,1__weibo__7.12.2__iphone__os11.1&ft=0&aid=01Av9tn9LLqR5apU_SfKnDUAO9Wacfs76KIEBqPTg2v5UOHNk.&uicode=10000198&itemid=2306186004281123_-_APPLICATION&featurecode=10000001&luicode=10000001&fromlog=100016406721847&fid=2302836004281123&lfid=100016406721847")
        for param_k,param_v in url_param.items():
            cururl_para[param_k] = param_v
        cururl_para["itemid"] = "230618"+uid+"_-_APPLICATION"
        cururl_para["fid"] = "230618"+uid
        url = "https://api.weibo.cn/2/container/get_item?" + urllib.urlencode(cururl_para)
        url_content = tool.getUrlContent(url)

        cururl_para["itemid"] = "230618"+uid+"_-_HOTMBLOG"
        cururl_para["fid"] = "230283"+uid
        url = "https://api.weibo.cn/2/container/get_item?" + urllib.urlencode(cururl_para)
        url_content = tool.getUrlContent(url)


        cururl_para["itemid"] = "230618"+uid+"_-_TOPICLIST"
        url = "https://api.weibo.cn/2/container/get_item?" + urllib.urlencode(cururl_para)
        url_content = tool.getUrlContent(url)

        cururl_para["itemid"] = "230618"+uid+"_-_ARTICLE"
        url = "https://api.weibo.cn/2/container/get_item?" + urllib.urlencode(cururl_para)
        url_content = tool.getUrlContent(url)

        cururl_para["itemid"] = "230618"+uid+"_-_HONGBAOCARD"
        url = "https://api.weibo.cn/2/container/get_item?" + urllib.urlencode(cururl_para)
        url_content = tool.getUrlContent(url)
        return url_content


    #浏览用户信息
    def __person_profile(self,url_param,uid):

        self.rand_url()
        userinfo_param = tool.url2Dict("https://api.weibo.cn/2/profile?gsid=_2A253UqW1DeRxGeBK61QW8i_EzzuIHXVSSb59rDV6PUJbkdANLRHwkWpNR_4pDT5xGeh3D3L_tq3fphqWEtcPPV_8&wm=3333_2001&i=9b17ad6&b=0&from=107C293010&c=iphone&networktype=wifi&v_p=56&skin=default&v_f=1&s=3c8f3a0a&lang=zh_CN&sflag=1&ua=iPhone9,1__weibo__7.12.2__iphone__os11.1&ft=0&aid=01Av9tn9LLqR5apU_SfKnDUAO9Wacfs76KIEBqPTg2v5UOHNk.&uicode=10000198&moduleID=pagecard&featurecode=10000001&mid=4195012604100383&luicode=10000001&_status_id=4195012604100383&rid=0_0_8_3080955430742652852&fromlog=100016406721847&user_domain=6004281123&lfid=100016406721847&profile_entry_key=1")
        for param_k,param_v in url_param.items():
            userinfo_param[param_k] = param_v
        userinfo_param["user_domain"] = uid
        profile_url = "https://api.weibo.cn/2/profile?" + urllib.urlencode(userinfo_param)
