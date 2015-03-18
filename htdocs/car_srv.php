<?php

$cars = array("193.2.178.98:80", "193.2.177.130:12345");
//$cars = array("193.2.178.98:80", "192.168.1.108:12345");
//$cars = array("193.2.178.98:80", "192.168.1.148:80");

//$request = "http://" . $cars[$_GET["id"]] . "/?command=" . $_GET["command"];
$request = "http://" . $cars[$_GET["id"]] . "/?up=" . $_GET["up"] . "&down=" . $_GET["down"] . "&left=" . $_GET["left"] . "&right=" . $_GET["right"0] . "&time=" . $_GET["time"];
$output = file_get_contents($request);

header("Access-Control-Allow-Origin: *");
echo $output;

?>