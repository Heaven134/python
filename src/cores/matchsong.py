# /usr/env python
# -*- coding: UTF-8 -*-


class MatchSong:
        
        def __init__(self,matchsongid,actid,songid,promotion,suggest,listen,vote=0,thumb=0,score=0,visible_rank_score=0,visible_listen_num=0,visible_vote_num=0,visible_thumb_num=0,order_no=0,vote_score=0,listen_score=0,collect_score=0,visible_vote_score=0,visible_listen_score=0,visible_collect_score=0,visible_quantity_1=0,visible_quantity_2=0,visible_quantity_3=0,visible_quantity_4=0,visible_quantity_5=0,visible_quantity_6=0,visible_score_1=0,visible_score_2=0,visible_score_3=0,visible_score_4=0,visible_score_5=0,visible_score_6=0):
                self.matchsongid = matchsongid #matchsong 表的id ，用于取代歌曲的上传时间，id小的上传时间早
                self.actid  = actid
                self.songid = songid  
                self.score = score
                self.listen = listen 
                self.vote = vote
                self.thumb = thumb
                self.promotion = promotion
                self.visible_rank_score = visible_rank_score
                self.visible_listen_num = visible_listen_num
                self.visible_vote_num = visible_vote_num
                self.visible_thumb_num = visible_thumb_num
                self.order_no = order_no
                self.suggest = suggest
                self.vote_score=vote_score
                self.listen_score = listen_score
                self.collect_score = collect_score
                self.visible_vote_score = visible_vote_score
                self.visible_listen_score = visible_listen_score
                self.visible_collect_score = visible_collect_score
                self.visible_quantity_1 = visible_quantity_1
                self.visible_quantity_2 = visible_quantity_2
                self.visible_quantity_3 = visible_quantity_3
                self.visible_quantity_4 = visible_quantity_4
                self.visible_quantity_5 = visible_quantity_5
                self.visible_quantity_6 = visible_quantity_6
                self.visible_score_1 = visible_score_1
                self.visible_score_2 = visible_score_2
                self.visible_score_3 = visible_score_3
                self.visible_score_4 = visible_score_4
                self.visible_score_5 = visible_score_5
                self.visible_score_6 = visible_score_6
                
        def __cmp__(self,other):
                if self.score > other.score:
                        return -1
                elif self.score == other.score:
                        if  self.vote_score > other.vote_score:
                                return -1
                        elif self.vote_score == other.vote_score:
                                if self.collect_score > other.collect_score:
                                        return -1
                                elif self.collect_score == other.collect_score:
                                        if self.listen_score > other.listen_score:
                                                return -1
                                        elif self.listen_score == other.listen_score:
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
                                        return 1
                        else:
                                return 1
                else:
                        return 1
        def __str__(self):
                return "matchsongid:"+str(self.matchsongid)+"  actid:"+str(self.actid)+" songid:"+str(self.songid) + " score: "+ str(self.score) + " listen : " + str(self.listen)+ " vote "+ str(self.vote)+ " thumb : " + str(self.thumb) + " orderno: "+ str(self.order_no) + ' vir_listen_num'+str(self.visible_listen_num) +' vir_vote_num :' + str(self.visible_vote_num) + '   visible_thumb_num :'+str(self.visible_thumb_num) +' visible_rank_score ' +str(self.visible_rank_score) +' visible_quantity_1 ' +str(self.visible_quantity_1) +' visible_score_1 ' +str(self.visible_score_1) +' visible_quantity_2 ' +str(self.visible_quantity_2) +' visible_score_2 ' +str(self.visible_score_2) +' visible_quantity_3 ' +str(self.visible_quantity_3) +' visible_score_3 ' +str(self.visible_score_3) +' visible_quantity_4 ' +str(self.visible_quantity_4) +' visible_score_4 ' +str(self.visible_score_4) +' visible_quantity_5 ' +str(self.visible_quantity_5) +' visible_score_5 ' +str(self.visible_score_5) +' visible_quantity_6 ' +str(self.visible_quantity_6) +' visible_score_6 ' +str(self.visible_score_6)

