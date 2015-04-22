<!DOCTYPE html>

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
				$tmp_car[trim($tmp1[0])] = trim($tmp1[1]);
			}
			$tmp_car["id"] = $id_co;
		}
		fclose($fajl);
		$cars[$id_co] = $tmp_car;
		$id_co += 1;
	}
}
?>

<html>
<head>
	<title>Communication test</title>
	<link rel="stylesheet" type="text/css" href="styles/main.css"/>
	<script src="scripts/jquery-2.1.3.min.js"></script>
	<script src="scripts/commMobile.js"></script>
</head>

<body>
<div class="content">
	<h1>Communication example</h1>
	
	<div class="carSelection">
		Avto:
		<select id="cars_list">
			<?php
			foreach($cars as $car){
				echo "<option name=car_option value=".$car["ip"].":".$car["port"].">".trim($car["name"])."</option>";
			}
			?>
		</select>
	</div>
	<button id = "wsconnect" type="button">Connect</button>
</div>

<div id="orientout">
</div>

<div id="backward"></div>
<div id="forward"></div>

</body>
</html>