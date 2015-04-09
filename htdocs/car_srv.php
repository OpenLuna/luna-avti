<?php


$all_cars = scandir("cars/");
$cars = array();
$id_co = 0;
foreach ($all_cars as $car) {
	$tmp_car = array();
	$tmp = explode(".", $car)[0];
	if (strcmp($tmp, "") !== 0){
		$fajl = fopen("cars/".$car, "r");
		if($fajl){
			while (($line = fgets($fajl)) !== false ){
				$tmp1 = explode(":", $line);
				$tmp_car[$tmp1[0]] = $tmp1[1];
			}
			$tmp_car["id"] = $id_co;
		}
		fclose($fajl);
	}
	$cars[$id_co] = $tmp_car;
	$id_co += 1;
}

$request = "http://" . trim($cars[$_GET["id"]]["ip"]) . ":". trim($cars[$_GET["id"]]["port"]) . "/?up=" . $_GET["up"] . "&down=" . $_GET["down"] . "&left=" . $_GET["left"] . "&right=" . $_GET["right"] . "&time=" . $_GET["time"];

$curl_handle=curl_init();
curl_setopt($curl_handle, CURLOPT_URL,$request);
curl_setopt($curl_handle, CURLOPT_CONNECTTIMEOUT, 2);
curl_setopt($curl_handle, CURLOPT_RETURNTRANSFER, 1);
$start_time_all = microtime(true); //timer ALL
$query = curl_exec($curl_handle);
curl_close($curl_handle);
$ex_time_all = microtime(true) - $start_time_all; //timer ALL
header("Access-Control-Allow-Origin: *");
echo "OK";


$file = fopen("logs/log".$_GET["id"].".csv", "a");
$data = array(trim($cars[$_GET["id"]]["name"]), $_GET["time"], "PHP-all", $ex_time_all);
fputcsv($file, $data);
fclose($file);
?>