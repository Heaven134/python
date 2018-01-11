1.  bin目录为脚本执行目录
    1.1  main.py 为为计算榜单得分的脚本，会将当天在线的活动的所有得分重新计算，目前线上是每个小时执行一次，16 * * * *
    1.2  default.py 计算默认列表（打榜列表），将结果放入redis
    1.3  hot。py 计算热榜列表
    1.4  reCalcScore.py 重新计算所有活动的得分，和main.py的区别就是，main.py会重新计算日志，从 api接口获取投票信息计算得分，reCalcScore.py只计算数据库里的数据，
    	 这个脚本是打算给mis用的，mis在改完晋级的人数之后，调用该脚本立即计算得分，但是目前还没有部署，里面有一些算法还不是最新的,没来得及改。相对main.py
    1.5 start.sh 拉取日志，合并日志，然后调用user_act.py，user_act.py内部循环调用user_act.sh，用于计算用户动态
2. conf目录
    1.1 config.py 设置配置信息：
    	dbconf 数据库配置
    	redisconf redis配置
    	apiconf ：获取投票，点赞的api配置
    	listen_log_path ：日志解析的时候，解析的日志
          
    
    		