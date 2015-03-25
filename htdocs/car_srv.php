<?php
start_session();
//$start_time = microtime();
//$cars = array("193.2.178.98:80", "193.2.177.130:12345");
//$cars = array("193.2.178.98:80", "192.168.1.108:12345");
//$cars = array("193.2.178.98:80", "192.168.1.148:80");
$cars = $_SESSION["cars"];

//$request = "http://" . $cars[$_GET["id"]] . "/?command=" . $_GET["command"];
$request = "http://" . $cars[$_GET["id"]]["ip"] .":".$cars[$_GET["id"]]["port"] . "/?up=" . $_GET["up"] . "&down=" . $_GET["down"] . "&left=" . $_GET["left"] . "&right=" . $_GET["right"] . "&time=" . $_GET["time"];
$output = file_get_contents($request);

header("Access-Control-Allow-Origin: *");
//$ex_time = microtime() - $start_time;
//$file = fopen("logs/log.csv", "w");
//$data = array()
//fputcsv($file, explode(',', ))

echo $output;

?>