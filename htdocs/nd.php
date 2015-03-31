<?php
//ip/?nb=true
session_start();
$cars = $_SESSION["cars"];
$phpLog = array();
$handle = fopen("logs/log".$_POST["id"].".csv", "r");
while (($data = fgetcsv($handle)) !== FALSE){
	$tmp = array();
	foreach($data as $d){
		$tmp[] = $d;
	}	
	$phpLog[] = $tmp;
}

$request = "http://" . trim($cars[$_POST["id"]]["ip"]) . ":". trim($cars[$_POST["id"]]["port"]) . "/?nd=true";
$output = file_get_contents($request);
//treba je narest explode pa dat v tabelo
//echo $_POST['id'];
echo $_POST['data'];

/*
* damo vse v isto tabelo, sortiramo po time
*/

?>