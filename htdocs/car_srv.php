<?php
session_start();
$start_time = microtime(true);
$cars = $_SESSION["cars"];
$request = "http://" . trim($cars[$_GET["id"]]["ip"]) . ":". trim($cars[$_GET["id"]]["port"]) . "/?up=" . $_GET["up"] . "&down=" . $_GET["down"] . "&left=" . $_GET["left"] . "&right=" . $_GET["right"] . "&time=" . $_GET["time"];
$output = file_get_contents($request);

header("Access-Control-Allow-Origin: *");
$ex_time = microtime(true) - $start_time;
if($ex_time < 0){
	$file = fopen("logs/t.csv", "a");
	fwrite($file, $start_time . " " . microtime() . "\n");
	fclose($file);
}
$file = fopen("logs/log.csv", "a");
$data = array(trim($cars[$_GET["id"]]["name"]), $_GET["time"], "PHP", $ex_time);
echo fputcsv($file, $data);
fclose($file);
?>