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
						$tmp_car[$tmp1[0]] = $tmp1[1];
					}
					$tmp_car["id"] = $id_co;
				}
				fclose($fajl);
			}
			$cars[$id_co] = $tmp_car;
			$id_co += 1;
		}
?>
<script>
	var cars = <?php echo json_encode($cars); ?>;
</script>
<html>
<head>
	<title>Communication test</title>
	<link rel="stylesheet" type="text/css" href="main.css"/>
	<script src="jquery-2.1.3.min.js"></script>
	<script src="jquery.redirect.js"></script>
	<script src="comm1.js"></script>
	<script src="http://jwpsrv.com/library/udi9iLWzEeSQBgp+lcGdIw.js"></script>
</head>
<body>

<div class="content">
	<h1>Communication example</h1>
	

	<div class="carSelection">
		Avto:
		<select id="cars_list">
			<!-- nekako: <option> Avto </option> -->
			<?php
				foreach($cars as $car){
					if ($car["name"]){
						echo "<option name=car_option value=".$car["id"].">".trim($car["name"])."</option>";
					}
				}
			?>
		</select>
	</div>
	<button id = "nd" type="button">Show network diagnostics</button>

	<div style="width:640px;margin:auto">
		<p id = "container1">Please install the Flash Plugin</p>
	</div>
	
	<script type = "text/javascript">
		jwplayer("container1").setup({
			file: "rtmp://212.235.189.232/flvplayback/ts_2_0_256",
			width: 640,
			height: 480,
			rtmp: {
				bufferlength: 0.05
			}
		});
	</script>
	
	<table class="commands">
		<tr>
			<td></td>
			<td id="buttonUp" class="full">up</td>
			<td></td>
		</tr>
		<tr>
			<td id="buttonLeft" class="full">left</td>
			<td id="buttonDown" class="full">down</td>
			<td id="buttonRight" class="full">right</td>
		</tr>
	</table>

	Result: <span id="ajax-result">send a message ...</span>
</div>

</body>
</html>