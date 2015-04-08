<link rel="stylesheet" href="//cdn.datatables.net/1.10.6/css/jquery.dataTables.min.css"/>
<script src="jquery-2.1.3.min.js"></script>
<script src="//cdn.datatables.net/1.10.6/js/jquery.dataTables.min.js"></script>


<script>
$(document).ready(function(){
    $('#tabela').DataTable();
});
</script>

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

//RASPBERRY PI LOG
$request = "http://" . trim($cars[$_POST["id"]]["ip"]) . ":". trim($cars[$_POST["id"]]["port"]) . "/?nd=true";
$curl_handle=curl_init();
curl_setopt($curl_handle, CURLOPT_URL,$request);
curl_setopt($curl_handle, CURLOPT_CONNECTTIMEOUT, 2);
curl_setopt($curl_handle, CURLOPT_RETURNTRANSFER, 1);
$output = curl_exec($curl_handle);
curl_close($curl_handle);
$piLog = array();
foreach (explode("\n", $output) as $line){
	$piLog[] = explode(",", $line);
}
array_pop($piLog);

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
	foreach ($piLog as $pi){
		if (count($pi) != 4){
			echo "nekI";
			print_r($pi);
		}
		if ($pi[1] == $tmp[1]){
			$tmp[] = $pi[2];
			$tmp[] = number_format($pi[3], 10);
		}
	}
	
	$fullLog[] = $tmp;
}

echo "<table id='tabela' border='1'>";
echo "<thead><tr><th>Avto</th><th>ID</th><th>Overall</th><th>ČAS A</th><th>ČAS B</th><th>PiProg</th></tr></thead>";
echo "<tdata>";
foreach ($fullLog as $entry){
	$s = "<tr>";
	$s .= "<td>".$entry[0]."</td>";//AVTO
	$s .= "<td>".$entry[1]."</td>";//ID
	$s .= "<td>".$entry[3]."</td>";//Overall
	$s .= "<td>".($entry[3]-$entry[5])."</td>";//CAS A
	$s .= "<td>".($entry[7]+$entry[9])."</td>";//CAS B
	$s .= "<td>".($entry[11]-$entry[7]-$entry[9])."</td>";//PiProg
	$s .= "</tr>";	
	echo $s;
}
echo "</tdata></table>";

?>