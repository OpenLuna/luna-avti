<?php
//ip/?nb=true
$phpLog = array();
$handle = fopen("logs/log".$_POST["id"].".csv", "r");
while (($data = fgetcsv($handle)) !== FALSE){
	$tmp = array();
	foreach($data as $d){
		$tmp[] = $d;
	}	
	$phpLog[] = $tmp;
}
/*
session_start();
$start_time = microtime(true);
$cars = $_SESSION["cars"];
$request = "http://" . trim($cars[$_POST["id"]]["ip"]) . ":". trim($cars[$_GET["id"]]["port"]) . "/?nd=true";
$output = file_get_contents($request);
echo $_POST['id'];
echo $_POST['data'];
*/
?>