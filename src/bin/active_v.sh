function active_v()
{
    log_prefix=$1
    log_date=$2
    activity=$3
    hour=0
    while [ $hour -lt 24 ]
    do
        str=`printf "%02d" $hour`
        file_name=$log_prefix$log_date$str
        cat $file_name >> temp_day
        hour=`expr $hour + 1`
    done
    ak="\["$activity"_"
    tempfile=$file".tmp"
    grep $ak $file | egrep '(log_song_play|add_thumb)'|awk '{print $14}'>$tempfile
    egrep '(3\]|3_add_thumb)' $tempfile|awk -F'_' '{print $3}'|>v_act
    tail -500 v_act|tac > v_act_r
    cnt=1
    cat v_act_r|while read item
    do
        if [ $cnt -gt 10 ];then
            break
        fi
        if [ $cnt -gt 0 ];then
            fk="\b$item\b"
            have_item=`egrep $fk vv|awk '{print $1}'|wc -l`
            if [ $have_item -eq 0 ];then
                echo $item>>vv
                cnt=`expr $cnt + 1`
            fi
        else
            echo $item>>vv
            cnt=`expr $cnt + 1`
        fi
    done
}
