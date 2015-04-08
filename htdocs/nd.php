<?php
session_start();
$cars = $_SESSION["cars"];

//SERVER LOG
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
//RASPBERRY PI LOG
$request = "http://" . trim($cars[$_POST["id"]]["ip"]) . ":". trim($cars[$_POST["id"]]["port"]) . "/?nd=true";
$output = file_get_contents($request);
//treba je narest explode pa dat v tabelo
$piLog = array();
foreach (explode("\n", $output) as $line){
	$piLog[] = explode(",", $line)
}
*/
//FRONTEND LOG
$jsLog = array();
foreach (explode("\n", $_POST['data']) as $line){
	$jsLog[] = explode(",", $line);
}

//MERGE
$fullLog = array();
foreach ($jsLog as $neki){
	$tmp = $neki;
	foreach ($phpLog as $php){
		if ($php[1] == $tmp[1]){
			$tmp[] = $php[2];
			$tmp[] = number_format($php[3], 10);
		}
	}
	/* ODKOMENTIRAJ ZA PI
	foreach ($piLog as $pi){
		if ($pi[1] == $tmp[1]){
			$tmp[] = $pi[2];
			$tmp[] = number_format($pi[3], 10);
		}
	}
	*/

	$fullLog[] = $tmp;
}

echo "<table border='1'>";
echo "<tr><th>Avto</th><th>ID</th><th>Kategorija</th><th>Čas</th><th>Kategorija</th><th>Čas</th><th>Kategorija</th><th>Čas</th><th>ČAS A</th><th>ČAS B</th></tr>";
foreach ($fullLog as $entry){
	$s = "<tr>";
	foreach ($entry as $en){
		$s .= "<td>".$en."</td>";		
	}
	$s .= "<td>".($entry[3]-$entry[5])."</td>";//."<td>".($entry[5]-$entry[7])."</td>"; //ODKOMENTIRAJ ZA PI
	$s .= "</tr>";	
	echo $s;
}
echo "</table>";

?>