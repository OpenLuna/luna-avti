<?php

session_start();
$cars = $_SESSION["cars"];
$request = "http://" . trim($cars[$_GET["id"]]["ip"]) . ":". trim($cars[$_GET["id"]]["port"]) . "/?up=" . $_GET["up"] . "&down=" . $_GET["down"] . "&left=" . $_GET["left"] . "&right=" . $_GET["right"] . "&time=" . $_GET["time"];
$start_time = microtime(true);
$curl_handle=curl_init();
curl_setopt($curl_handle, CURLOPT_URL,$request);
curl_setopt($curl_handle, CURLOPT_CONNECTTIMEOUT, 2);
curl_setopt($curl_handle, CURLOPT_RETURNTRANSFER, 1);
$query = curl_exec($curl_handle);
curl_close($curl_handle);
$ex_time = microtime(true) - $start_time;
header("Access-Control-Allow-Origin: *");

if($ex_time < 0){
	$file = fopen("logs/t.csv", "a");
	fwrite($file, $start_time . " " . microtime() . "\n");
	fclose($file);
}
$file = fopen("logs/log".$_GET["id"].".csv", "a");
$data = array(trim($cars[$_GET["id"]]["name"]), $_GET["time"], "PHP", $ex_time);
fclose($file);
echo "OK";
?>