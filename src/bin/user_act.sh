function user_act()
{
    file=$1
    activity=$2
    ak="_"$activity"_"
    tempfile=$file".tmp"
    grep $ak $file | egrep '(log_song_play|add_collect)'|awk '{print $9,$14}'>$tempfile
    filesize=`cat $tempfile |wc -l`
    if [ $filesize -eq 0 ];then
        echo "not data found"
        return
    fi
    sed -i 's/_/ /g' $tempfile
    sed -i 's/]//g' $tempfile
    tac $tempfile>tac.tmp
    mv tac.tmp $tempfile
    awk '
    BEGIN {vcnt=0; ucnt=0; actcnt=0;}
    {
       if($2 ~ /song/)
           action = 1;
       else
           action = 2;
       if(!($7 in users))
       {
           if($8 == 1)
           {
               if(vcnt<4)
               {
                   vcnt++;
                   actcnt++;
                   printf("%d,%d,%d,%d\n",$8,$6,action,$7);
               }
           }
           else if($8 == 0)
           {
               if(actcnt<10)
               {
                   ucnt++;
                   actcnt++;
                   printf("%d,%d,%d,%d\n",$8,$6,action,$7);
               }
           }
           users[$7]=1;
       }
    }' $tempfile>res.$2
    rescnt=`cat res.old.$2 res.$2|wc -l`
    if [ $rescnt -eq 0 ];then
        echo "not data found2"
        return
    fi
    vcnt=`grep ^1 res.$2|wc -l`
    if [ $vcnt -lt 4 ];then
        if [ $vcnt -eq 0 ];then
            echo "no Vuser"
            grep ^1 res.old.$2 |head -4>>res.cmd.$2
        else
            vk=`grep ^1 res.$2 |awk -F, '{printf("%d|",$4)}'|sed 's/|$//'`
            grep ^1 res.old.$2 |egrep -v $vk >>res.$2
            grep ^1 res.$2|head -4>res.cmd.$2
        fi
        v_cnt=`cat res.cmd.$2|wc -l`
        u_cnt=`expr 10 - $v_cnt`
        grep ^0 res.$2|head -$u_cnt >>res.cmd.$2
    else
        ucnt=`expr 10 - $vcnt`
        grep ^1 res.$2>res.cmd.$2
        grep ^0 res.$2|head -$ucnt>>res.cmd.$2
    fi
    total=`cat res.cmd.$2|wc -l`
    if [ $total -lt 10 ];then
        append=`expr 10 - $total`
        uk=`grep ^0 res.$2 |awk -F, '{printf("%d|",$4)}'|sed 's/|$//'`
        grep ^0 res.old.$2 |egrep -v $uk |head -$append>>res.cmd.$2
    fi

    cp res.cmd.$2 res.old.$2
    sed -i 's/[01],//' res.cmd.$2
    cat res.cmd.$2|tr "\n" "|" >res.cmd.$2.tmp
    mv res.cmd.$2.tmp res.cmd.$2
    sed -i "s/^/set activity$activity /" res.cmd.$2
    sed -i 's/|$//' res.cmd.$2
    #redis-cli -h 192.168.217.11 <res.cmd.$2
    redis-cli -h 10.16.87.99  -p 9003 <res.cmd.$2
    mv res.cmd.$2 res.cmd.$2.bak
}

user_act $1 $2
