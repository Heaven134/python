<?php
/**
 * @abstract http请求类
 * @author yanyugang<yanyugang@baidu.com>
 * @since 2010-12-15
 */
class DBHttpProxy
{
	const CONNECT_TIMEOUT = 1000;//连接超时时间，单位ms，利用curl时不能小于1000
	const TIMEOUT = 1000;//交互超时时间，单位ms

	/**
	 * GET请求
	 *
	 * @param string $url 请求的url
	 * @param bool $isHttps 是否是https
	 * @return string 返回运行结果
	 */
	public static function get($url, $isHttps = false)
	{
		return self::request($url, array(), 'GET', $isHttps);
	}
	
	
	/**
	 * POST请求
	 *
	 * @param string $url 请求的url
	 * @param array $data 请求传输的数据
	 * @param bool $isHttps 是否是https
	 * @return string 返回运行结果
	 */
	public static function post($url, $data, $isHttps = false)
	{
		return self::request($url, $data, 'POST', $isHttps);
	}
		
	
	/**
	 * request请求（GET || POST）
	 *
	 * @param string $url 请求的url
	 * @param array $data 请求传输的数据
	 * @param string $method 请求的方法：GET || POST
	 * @param bool $isHttps 是否是https
	 * @param int $linkTime 连接时间,单位秒
	 * @param int $dealTime 处理时间,单位秒
	 * @return string 返回运行结果
	 */
	public static function request($url, $data = array(), $method  = 'GET', $isHttps = false, $cookie = NULL, $linkTime=1, $dealTime=1, $httpHeader= array())
	{

	    $ch = curl_init();
	    $curlOptions = array(
		    CURLOPT_URL				=>	$url,
		    CURLOPT_CONNECTTIMEOUT	=>	$linkTime,
		    CURLOPT_TIMEOUT			=>	$dealTime,
		    CURLOPT_RETURNTRANSFER	=>	true,
		    CURLOPT_HEADER			=>	false,
		    CURLOPT_FOLLOWLOCATION	=>	true,
		    CURLOPT_HTTPHEADER		=>  $httpHeader,
		    CURLOPT_USERAGENT => 'tingapi',
	    ); 


	    if($method === 'POST'){
		$curlOptions[CURLOPT_POST] = true;
	    }
	    if($method === 'PUT'){
		$curlOptions[CURLOPT_PUT] = true;
	    }

	    if('POST' === $method || 'PUT' === $method)
	    {
		if(is_array($data))
		{
		    $curlOptions[CURLOPT_POSTFIELDS] = http_build_query($data);
		}else
		{
		    $curlOptions[CURLOPT_POSTFIELDS] = $data;
		}
	    }
	    if(true === $isHttps)
	    {
		$curlOptions[CURLOPT_SSL_VERIFYPEER] = false;
	    }
	    if(isset($cookie))
	    {
		$curlOptions[CURLOPT_COOKIE] = $cookie;
	    }
	    curl_setopt_array($ch, $curlOptions);
	    $response = curl_exec($ch);
	    $errno = curl_errno($ch);
	    if(0 != $errno)
	    {
		curl_close($ch);

		return false;
	    }

	    curl_close($ch);

	    return $response;
	}
	
	public static function buidQueryStr($query){
		$str = "";
		foreach ($query as $key => $value){
			$str .= "{$key}={$value}&";
		}
		return trim($str,'&');
	}
}
?>
