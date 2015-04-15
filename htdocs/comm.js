var keysdown = {};
var LEFT = 74; //j
var RIGHT = 76; //l
var UP = 73; //i
var DOWN = 75; //k
var ON = "ON";
var OFF = "OFF";
var SERVER_URL = "http://" + document.URL.split("/")[2] + "/car_srv.php";
var websocket = null;

function wsConnect(){
	if(websocket != null){
		websocket.close();
	}
	else{
		var carURL = "ws://" + $("#cars_list option:selected").val();
		websocket = new WebSocket(carURL);
		websocket.onopen = function(evt){
			$("button#wsconnect").text("Disconnect");
		};
		websocket.onclose = function(evt){
			$("button#wsconnect").text("Connect");
			websocket = null;
		};
		websocket.onmessage = function(evt){
			console.log(evt);
		};
		websocket.onerror = function(evt){
			console.log(evt);
		};
	}
}

var sendState = function() {
	if(websocket == null) return;
	
	var left = (keysdown[LEFT] === true) ? ON : OFF;
	var right = (keysdown[RIGHT] === true) ? ON : OFF;
	var up = (keysdown[UP] === true) ? ON : OFF;
	var down = (keysdown[DOWN] === true) ? ON : OFF;
	var timestamp = (new Date()).getTime();
	
	var cmd = "?up=" + up + "&down=" + down + "&left=" + left + "&right=" + right + "&time=" + timestamp;
	websocket.send(cmd);
}

var handledown = function(e) {
	//console.log(e);
	if (keysdown[e.which] ==  false || (typeof keysdown[e.which] === "undefined")) {
		keysdown[e.which] = true;
		switch (e.which) {
			case UP:
				sendState();
				$("#buttonUp").css({backgroundColor: "green"});
				break;
			case LEFT:
				sendState();
				$("#buttonLeft").css({backgroundColor: "green"});
				break;
			case DOWN:
				sendState();
				$("#buttonDown").css({backgroundColor: "green"});
				break;
			case RIGHT:
				sendState();
				$("#buttonRight").css({backgroundColor: "green"});
				break;
		}
	}
}

var handleup = function(e) {
	//console.log(e);
	keysdown[e.which] = false;
	switch (e.which) {
		case UP:
			sendState();
			$("#buttonUp").css({backgroundColor: "lightblue"});
			break;
		case LEFT:
			sendState();
			$("#buttonLeft").css({backgroundColor: "lightblue"});
			break;
		case DOWN:
			sendState();
			$("#buttonDown").css({backgroundColor: "lightblue"});
			break;
		case RIGHT:
			sendState();
			$("#buttonRight").css({backgroundColor: "lightblue"});
			break;
	}
}

$(document).ready(function() {
	$(window).keydown(handledown).keyup(handleup);
	$("button#wsconnect").click(wsConnect);
});