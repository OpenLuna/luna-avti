<?php
$keys = array("name", "car_ip", "port");
foreach($keys as $key){
	if(!array_key_exists($key, $_GET)) die("Error while advertising: keyErr");
}

$file = fopen("cars/".$_GET["name"].".car", "w") or die("Error while advertising: fileErr");
fwrite($file, "name: ".$_GET["name"]."\n");
fwrite($file, "ip: ".$_GET["car_ip"]."\n");
fwrite($file, "port: ".$_GET["port"]."\n");
fclose($file);
echo "Car successfully advertised";
?>