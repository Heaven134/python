#!/bin/bash
#
#
#
scriptdir=$(cd "$(dirname "$0")"; pwd)


hosts=('192.168.1.251' '192.168.2.102' '192.168.1.250' '192.168.2.104')
targetdir=/home/work/heapi_nginx/logs/lua/
filename=lua.log.
localdir=/home/work/cron/tbang_rankservice/data
pythonpath=/home/work/local/python/bin/python

date=`date  -d '5 minutes ago' +%Y%m%d%H`

echo 'the date is '$date

cd $localdir
rm $filename$date*

for h in   ${hosts[@]} 
do
     url=ftp://${h}$targetdir$filename$date
     echo 'begin to wget the file '$url
     wget $url
     mv $filename$date $filename$date.${h}
done

cat $filename$date.* > $filename$date 
rm $filename$date.*


echo 'the script dir is  '$scriptdir
cd $scriptdir



#$pythonpath user_act.py  $localdir/$filename$date


#$pythonpath main.py

#sh user_act.sh $localdir/$filename$date 118
