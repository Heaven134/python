<?php
date_default_timezone_set('PRC');
define("RUNTIME", 'online');

$_dbConf = array(
    'test' => array(
	'hosts' => array('192.168.217.11'),
	'port' => 9306,
	'database' => 'heyinliang_api',
	'username' => 'root',
	'password' => 'baeapibae',
	'timeout' => 1, //sec
    ),
    'qa' => array(
	'hosts' => array('192.168.217.11'),
	'port' => 9306,
	'database' => 'heyinliang_api',
	'username' => 'root',
	'password' => 'baeapibae',
	'timeout' => 1, //sec
    ),
    'online' => array(
	'hosts' => array('10.16.192.200'),
	'port' => 6054,
	'database' => 'heyinliang_api',
	'username' => 'heyinliang_api_w',
	'password' => '6HuQWT3GC7uWCNZc',
	'timeout' => 1, //sec
    ),
);

function connect($conf){
    $host = $conf[RUNTIME]["hosts"][0];
    $port = $conf[RUNTIME]["port"];
    $database = $conf[RUNTIME]["database"];
    $username = $conf[RUNTIME]["username"];
    $password = $conf[RUNTIME]["password"];

    $db = mysql_connect($host.":".$port, $username,$password);
    mysql_select_db($database, $db);
    mysql_query("set names utf8", $db);

    return $db;
}

function _log($msg){
    echo '[' . date('Y-m-d H:i:s') . '] ' . $msg . "\n"; 
}

$db = connect($_dbConf);
$sql = "SELECT activity_id,start_time,end_time,status,match_no FROM he_activity WHERE status!=-1";
$ret = mysql_query($sql, $db);
if(!$ret)
{
    _log("connect mysql fail!!!");
    exit;
}

$time = time();
$activity_id_end = array();
$activity_id_start = array();
$activity_id_doing = array();
$activity_info = array();
while(($result = mysql_fetch_assoc($ret)))
{
    if(empty($result) ||  !is_array($result))
    {
	_log("get activity info empty!!!");
	exit;
    }

    //结束
    if($result["end_time"] <= $time && $result["status"] != -1) 
    {
        $activity_id_end[] = $result["activity_id"];
    }
    //开始
    if($result["start_time"] <= $time && $time <= $result["end_time"] && $result["status"] == 0) 
    {
        $activity_id_start[] = $result["activity_id"];
    }

    //正在进行
    if($result["start_time"] <= $time && $time <= $result["end_time"] && $result["status"] == 1)
    {
	$activity_id_doing[] = $result["activity_id"];
	$activity_info[$result["activity_id"]] = $result;
    }    
}

if(empty($activity_id_end) && empty($activity_id_start) && empty($activity_id_doing))
{
    _log("update nothing");
    exit;
}

//修改活动状态
if(!empty($activity_id_end))
{
    $sql = "UPDATE he_activity set status = -1 WHERE activity_id in (".implode(",", $activity_id_end).")";
    $ret = mysql_query($sql, $db);
    if($ret)
    {
	_log("update activity end status success...$sql");
    }else
    {
	_log("update activity end status fail!!!$sql");
    }
}

if(!empty($activity_id_start))
{
    $sql = "UPDATE he_activity set status = 1 WHERE activity_id in (".implode(",", $activity_id_start).");";
    $ret = mysql_query($sql, $db);
    if($ret)
    {
	_log("update activity doing status success...$sql");
    }else
    {
	_log("update activity doing status fail!!!$sql");
    }
}

//合并已经开始及正在进行活动ID
$activity_id_doing = array_merge($activity_id_start, $activity_id_doing);
if(empty($activity_id_doing))
{
    _log("no activity match need to change.");
    exit; 
}

//模拟数据
//$activity_id_doing = array(132,133);
//

//征歌信息
$sql_solicit = "SELECT activity_id,start_time,end_time FROM he_activity_solicit WHERE activity_id in (".implode(",", $activity_id_doing).")";
$ret = mysql_query($sql_solicit, $db);
while(($result = mysql_fetch_assoc($ret)))
{
    $result["match_no"] = 0;
    $result["match_title"] = "征歌";
    $solicit_ret[] = $result;
}

//比赛信息
$sql_match = "SELECT activity_id,match_no,match_title,start_time,end_time,song_limit_num,status FROM he_activity_match WHERE activity_id in (".implode(",", $activity_id_doing).")";
$ret = mysql_query($sql_match, $db);
while(($result = mysql_fetch_assoc($ret)))
{
    $match_ret[] = $result;
}

if(!empty($solicit_ret) && is_array($solicit_ret))
{
    foreach($solicit_ret as $key=>$value)
    {
	$activity_ret[$value["activity_id"]][$value["match_no"]] = $value;
    }
}

if(!empty($match_ret) && is_array($match_ret))
{
    foreach($match_ret as $key=>$value)
    {
	$activity_ret[$value["activity_id"]][$value["match_no"]] = $value;
    }
}

if(empty($activity_ret) || !is_array($activity_ret))
{
    _log("activity_ret empty!");
    exit;
}

foreach($activity_ret as $key=>$value)
{
    $activity_match_no = 0;	//活动比赛阶段
    $activity_list_flag = 0;    //活动揭榜标示
    foreach($value as $k=>$v) 
    {
	$match_status = 0;
	if($v["start_time"] <= $time && $time <= $v["end_time"])
	{
	    $activity_match_no = $v["match_no"];
	    $match_status = 1;
	}else if($time>=$v["end_time"]){
	    $match_status = -1; 
	}	

	if($match_status == -1 && $v['match_no'] == 2)
	{
	    $activity_list_flag = 1;
	}

	//判断比赛状态默认status=0
	if($v["match_no"] != 0 && $match_status!=0 && $v["status"] != $match_status)
	{
	    $sql = "UPDATE he_activity_match SET status=$match_status WHERE activity_id=$key AND match_no={$v['match_no']} LIMIT 1";
	    $ret = mysql_query($sql, $db);
	    if($ret)
	    {
		_log("update he_activity_match success...$sql");
	    }else
	    {
		_log("update he_activity_match fail!!!$sql");
	    }
	}	
    }

    //复赛结束活动进入打榜阶段(因为复赛是最后一个阶段)
    if($activity_list_flag  == 1)
    {
	$sql = "UPDATE he_activity SET status=2 WHERE activity_id=$key LIMIT 1";
        $ret = mysql_query($sql, $db);
	if($ret)
	{
	    _log("update he_activity bill status success...$sql");
	}else
	{
	    _log("update he_activity bill status fail!!!$sql");
	}	
    }  

    //比赛进入复赛后(match_no=2)修改入围歌曲状态
    $match2no_limit_num = $value[2]["song_limit_num"];
    if($activity_match_no == 2)
    {
	$sql = "UPDATE he_activity_match_songs set match_no=$activity_match_no WHERE activity_id=$key AND match_no=1 AND order_no<=$match2no_limit_num LIMIT $match2no_limit_num";	
	$ret = mysql_query($sql, $db);
	if($ret)
	{
	    _log("update he_activity_match_songs  match_no success...$sql");
	}else
	{
	    _log("update he_activity_match_songs  match_no fail!!!$sql");
	}
    }

    //判断活动表里的match_no(默认是0征歌阶段)
    if($activity_match_no != 0 && $activity_info[$key]["match_no"] != $activity_match_no)
    {
        $sql = "UPDATE he_activity SET match_no=$activity_match_no WHERE activity_id=$key LIMIT 1";
        $ret = mysql_query($sql, $db);
	if($ret)
	{
	    _log("update he_activity match_no success...$sql"); 

	    //调用python脚本生成随机歌曲列表
	    if($activity_match_no == 1 || $activity_match_no == 2)
	    {
		_log("now exec python...");
		exec("/home/bae/.jumbo/bin/python /home/bae/ting/cron/hotcron/he/rankservice/src/bin/default.py");
		_log("exec python done...");
	    }
	}else
	{
	    _log("update he_activity match_no fail!!!$sql");
	}
    } 
}
_log("done..");
?>
