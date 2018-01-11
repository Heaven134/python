<?php
/**
 * 中奖服务逻辑主要分为3部分
 *
 * 1.活动结束后，计算活动的榜单，写入he_activity_rank_list表
 * 2.上榜歌曲的艺人进行分钱 
 * 3.猜中歌曲的用户进行分钱，目前分为一等奖，二等奖，三等奖
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

$_prizeConf = array(
    "song_num" => 10,		    //入围榜单歌曲数 
    "month_prize" => array(	    //月赛奖金
	1=> 100000,
	2=> 60000,
	3=> 40000,
	4=> 30000,
	5=> 20000,
	6=> 10000,
	7=> 10000,
	8=> 10000,
	9=> 10000,
	10=> 10000,
    ),
);

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


/**
 * 根据歌曲排名写入榜单表 he_activity_rank_list 
 *
 */

$db = connect($_dbConf);
$sql = "SELECT activity_id  FROM he_activity WHERE match_no = 2 and status=-1 ORDER BY activity_id DESC LIMIT 1";
$ret = mysql_query($sql, $db);
if(!$ret)
{
    _log("get mysql resource fail!!!");
    exit;
}

$activity_id_end = array();
while(($result = mysql_fetch_assoc($ret)))
{
    if(empty($result) ||  !is_array($result))
    {
	_log("get activity info empty!!!");
	exit;
    }

    $activity_id_end[] = $result["activity_id"];
}

if(empty($activity_id_end))
{
    _log("update nothing");
    exit;
}

$activity_id = $activity_id_end[0];

//查看榜单是否生成
$list_ret = array();
$sql = "SELECT activity_id, song_id FROM he_activity_rank_list WHERE activity_id=$activity_id limit 1";
$ret = mysql_query($sql, $db);
while(($result = mysql_fetch_assoc($ret)))
{
    $list_ret[] = $result;
}

if(!empty($list_ret) && is_array($list_ret))
{
    _log("activity_id $activity_id exist!");
    exit;
}

//获取入围榜单歌曲
$sql = "SELECT song_id,user_id,user_name,visible_listen_num,visible_rank_score,visible_vote_num,visible_thumb_num,order_no FROM he_activity_match_songs WHERE activity_id=$activity_id AND match_no=2 ORDER BY order_no ASC limit {$_prizeConf['song_num']}";
$ret = mysql_query($sql, $db);
while(($result = mysql_fetch_assoc($ret)))
{
    $list_ret[] = $result;
    $list_song_id[] = $result["song_id"];
}

$sql = "SELECT song_id,song_title,user_id,user_name FROM he_songs_info WHERE song_id in (".implode(",", $list_song_id).")";
$ret = mysql_query($sql, $db);
while(($result = mysql_fetch_assoc($ret)))
{
    $song_ret[] = $result;
}

if(empty($song_ret) && !is_array($song_ret))
{
    _log("song id not exist.".implode(" ",$list_song_id));
}

foreach($song_ret as $key=>$value)
{
    $song_info[$value["song_id"]] = $value;
}

foreach($list_ret as $key=>$value)
{
    if($song_info[$value["song_id"]])
    {
	$song_info[$value["song_id"]]["visible_listen_num"] = $value["visible_listen_num"];
	$song_info[$value["song_id"]]["visible_rank_score"] = $value["visible_rank_score"];
	$song_info[$value["song_id"]]["visible_vote_num"] = $value["visible_vote_num"];
	$song_info[$value["song_id"]]["visible_thumb_num"] = $value["visible_thumb_num"];
	$song_info[$value["song_id"]]["order_no"] = $value["order_no"];

	$song_order_info[] = $song_info[$value["song_id"]];
    }
}

//写入rank_list表
$rank_values = "";
$time = time();
foreach($song_order_info as $key=>$value)
{
    $rank_values .= "(5, $activity_id, {$value['song_id']}, '{$value['song_title']}', {$value['user_id']}, '{$value['user_name']}', {$value['visible_listen_num']}, {$value['visible_thumb_num']}, {$value['visible_vote_num']}, {$value['visible_rank_score']}, $time),";
}
$rank_values = rtrim($rank_values, ",");

$sql = "INSERT INTO he_activity_rank_list (topic_id, activity_id, song_id, song_title, user_id, user_name, listen_score, fav_score, vote_score, total_score, create_time) VALUES $rank_values";

$ret = mysql_query($sql, $db);
if($ret)
{
    _log("insert he_activity_rank_list success...$sql");
}else
{
    _log("insert he_activity_rank_list  fail!!!$sql");
}

/**
 * 上榜歌曲的艺人进行分钱 
 *
 */
$values = "";
$create_time = time();
$desposit_values = "";
foreach($song_order_info as $key=>$value)
{
    $prize_level = $value['order_no'];
    $prize_money = $_prizeConf['month_prize'][$prize_level];

    $desposit_values .= "({$value['song_id']}, 1, $activity_id, {$value['user_id']}, $prize_money, $prize_level, 0, $create_time),";
}

$desposit_values = rtrim($desposit_values, ",");
$desposit_sql = "INSERT INTO he_users_desposit (song_id, type, activity_id, user_id, money, prize_level, status, create_time) VALUES $desposit_values";

$ret = mysql_query($desposit_sql, $db);
if($ret)
{
    _log("insert he_activity_desposit success...$sql");
}else
{
    _log("insert he_activity_desposit  fail!!!$sql");
}


/**
 * 设置用户分奖标示 1-开始 -1-结束
 */
$redis = _redisConnect($_redisConf);
$user_prize_key = "he_activity_cron_usre_prize_status_$activity_id";
$user_prize_status = $redis->set($user_prize_key, 1)
if($user_prize_status == false)
{
    _log("user prize set status 1 fail.key:$user_prize_status");
}else
{
    _log("user prize set status 1 fail.key:$user_prize_status");
}

_log("done..");
?>
