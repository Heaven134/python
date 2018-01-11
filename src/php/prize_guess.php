<?php
/**
 * 用户猜歌中奖 
 *
 *  
 * 
 * 中奖规则参照 http://y.baidu.com/tbang活动规则
 *
 */
date_default_timezone_set('PRC');
define("RUNTIME", 'test');

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

$_redisConf = array(
    'test' => array(
	'hosts' => array('192.168.217.11'),
	'port' => 6379,
    ),
    'qa' => array(
	'hosts' => array('192.168.217.11'),
	'port' => 6379,
    ),
    'online' => array(
	'hosts' => array('192.168.217.11'),
	'port' => 6379,
    ),
);

$_baseUrl = array(
    'test' => array(
	'theme' => 'http://192.168.217.11:8258/theme/getsets',
    ),
    'qa' => array(
	'theme' => 'http://192.168.217.11:8258/theme/getsets',
    ),
    'online' => array(
	'theme' => 'http://192.168.217.11:8258/theme/getsets',
    )
);

$_prizeConf = array(
    "song_num" => 10,               //入围榜单歌曲数  
    "month_prize" => array(	    //月赛奖金
	1=> 50000,
	2=> 40000,
	3=> 30000,
	4=> 20000,
	5=> 10000,	
    ),
);


function _log($msg){
    echo '[' . date('Y-m-d H:i:s') . '] ' . $msg . "\n"; 
}

function _redisConnect($conf)
{
    $redis = new redis();

    $ip = $conf[RUNTIME]['hosts'][0];
    $port = $conf[RUNTIME]['port'];
    $redis_connect = $redis->connect($ip, $port);
    if(!$redis_connect)
    {
	_log("connect redis fail!!! ip:$ip port:$port");
	exit;
    }

    return $redis;
}

function _mysqlConnect($conf)
{
    $host = $conf[RUNTIME]["hosts"][0];
    $port = $conf[RUNTIME]["port"];
    $database = $conf[RUNTIME]["database"];
    $username = $conf[RUNTIME]["username"];
    $password = $conf[RUNTIME]["password"];

    $db = mysql_connect($host.":".$port, $username,$password);
    if(!$db)
    {
	_log("connect mysql fail:". mysql_error());
	exit;
    }

    mysql_select_db($database, $db);
    mysql_query("set names utf8", $db);

    return $db; 
}

/**
 * 获取刚结束的活动
 */
$db = _mysqlConnect($_dbConf);
$sql = "SELECT activity_id,end_time  FROM he_activity WHERE match_no = 2 and status=-1 ORDER BY activity_id DESC LIMIT 1";
$ret = mysql_query($sql, $db);
if(!$ret)
{
    _log("get mysql resource fail!!!");
    exit;
}

$activity_ret = array();
while(($result = mysql_fetch_assoc($ret)))
{
    if(empty($result) ||  !is_array($result))
    {
	_log("get activity info empty!!!");
	exit;
    }

    $activity_ret[] = $result;
}

if(empty($activity_ret))
{
    _log("nothing to do!");
    exit;
}

//活动结束一天之后默认奖品分配完
if(($activity_ret[0]['end_time'] + 86400) > time())
{
    _log("i guess user prize done!");
    exit;
}

$activity_id = $activity_ret[0]["activity_id"];

/**
 * 查看当期奖品是否需要分配
 */

$redis = _redisConnect($_redisConf);
$user_prize_key = "he_activity_cron_usre_prize_status_$activity_id";
$user_prize_ret = $redis->get($user_prize_key);
if($user_prize_ret == -1)
{
    _log("user prize done.key:$user_prize_key");
    exit;
}

if(!$user_prize_ret || $user_prize_ret == 0)
{
    _log("user prize waiting...key:$user_prize_key");
    exit;
}

/**
 * 查看榜单数据
 */

$sql = "SELECT activity_id,song_id  FROM he_activity_rank_list WHERE activity_id=$activity_id LIMIT {$_prizeConf['song_num']}";
$ret = mysql_query($sql, $db);

$activity_rank = array();
while(($result = mysql_fetch_assoc($ret)))
{ 
    $activity_rank[] = $result;
}

if(empty($activity_rank))
{
    _log("bill data not readyi!");
    exit;
}

//echo '<pre>';print_r($activity_rank);
//die;

/**
 * 猜中歌曲的用户进行分钱
 *
 */

set_include_path("/home/bae/zhangzilong/cron");
require 'DBHttpProxy.class.php';

$http_obj = new DBHttpProxy();

//
//模拟
//$activity_id = 110;
//$song_info = array(
//    array(
//	"song_id" => "10256",
//    ),
//    array(
//	"song_id" => "10257",
//    ),
//    array(
//	"song_id" => "10258",
//    ),
//);
//

$set_key = "he_activity_cron_guess_user_5_{$activity_id}";
$user_list_key_pre = "he_activity_cron_guess_user_5_{$activity_id}";
$error_no = 0;

foreach($activity_rank as $key=>$value)
{
    $vote_url = $_baseUrl[RUNTIME]["theme"]."?pid=heyinliang&tid=vote&actid=5_$activity_id&itemid={$value['song_id']}";    
    $ret = $http_obj->get($vote_url);
    if($ret == false)
    {
	$error_no = -1;

	_log("get vote_url fail:$vote_url");
	break;	
    }
    $vote_ret = json_decode($ret, 1);
    if(empty($vote_ret) || !is_array($vote_ret))
    {
	$error_no = -2;

	_log("json decode vot_url fail:$vote_url");
	break;
    }

    if($vote_ret["error_code"] && $vote_ret["error_code"] != 22000)
    {
	$error_no = -3;

	_log("response error_code error.error_code={$vote_ret["error_code"]} url:$vote_url");
	break;
    }

    if(!is_array($vote_ret['result']))
    {
	$error_no = -4;

	_log("response result not array.result:{$vote['result']} url:$vote_url");
	break;
    }

    if(empty($vote["result"]) && is_array($vote["result"]))
    {
	_log("no body hit this song. url:$vote_url");
	continue;
    }

    foreach($vote_ret["result"] as $k=>$v)
    {
	$zincrby_ret = $redis->zincrby($set_key, 1, $v['userid']);
	if($zincrby_ret == false)
	{
	    _log("set:guess_user member:{$v['userid']} zincrby fail!");  
	    continue;
	}

	//记录用户投中歌曲列表		
	$user_list_key = $user_list_key_pre."_".$v['userid'];
	$rpush_ret = $redis->rPush($user_list_key, $v['itemid']);
	if($rpush_ret == false)
	{
	    _log("rpush {$v['itemid']} into list {$user_list_key} fail!");  
	}
    }
}

if($error_no < 0)
{
    _log("get vote service error.error_no:$error_no");
}

/**
 * 计算获奖用户
 */
$set_count = $redis->zCount($set_key, 1, 10);
if($set_count == 0)
{
    _log("no body guess all the songs!");
    exit;
}

$step = 100;
$total_step = floor($set_count/$step) + 1;
$start = 0;
$end = 0 ;
$user_rank = array();
$user_rank_list = array();

for($i=1;$i<=$total_step;$i++)
{
    $start = ($i-1) * $step;    
    $end = ($i * $step) -1;
    $zrevrange_ret = $redis->zrevrange($set_key, $start, $end, true);

    foreach($zrevrange_ret as $key=>$value)
    {	
	$user_rank[$value] += 1;	
	$user_rank_list[$value][] = $key;	
    }

    if(count($user_rank) >= 5)
    {
	_log("got the guess user by $end. total level:5"); 
	break;
    }
}

_log("got the guess user by $end. total level:".count($user_rank));

/**
 * 将获奖用户写入到he_users_desposit表中
 */

$level = 0;
$desposit_values = "";
$create_time = time();

foreach($user_rank_list as $key=>$value)
{
    $level++; 
    $money = round($_prizeConf["month_prize"][$level] / $user_rank[$key], 2);
    $desposit_values = "";

    foreach($value as $k=>$v)
    {
	//获取用户投中song list
	$user_list_key = $user_list_key_pre."_".$v;
	$lrange_ret = $redis->lRange($user_list_key, 0, -1);
	$user_song_list = implode(",", $lrange_ret);

	$desposit_values .= "('{$user_song_list}', 2, $activity_id, $v, $money, $level, 0, $create_time),";
    }

    $desposit_values = rtrim($desposit_values, ",");

    $desposit_sql = "INSERT INTO he_users_desposit (song_id, type, activity_id, user_id, money, prize_level, status, create_time) VALUES $desposit_values";

    $ret = mysql_query($desposit_sql, $db);
    if($ret)
    {
        _log("insert he_activity_desposit success...$desposit_sql");
    }else
    {
        _log("insert he_activity_desposit  fail!!!$desposit_sql");
    }
}

/**
 * 设置结束标志位 -1
 */
$user_prize_end = $redis->set($user_prize_key, -1);
if($user_prize_end == false)
{
    _log("user prize set status -1 error. key:$user_prize_end");    
}else
{
    _log("user prize set status -1 success. key:$user_prize_end");    
}

_log("done..");
?>
