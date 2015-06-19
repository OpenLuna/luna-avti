var keysdown = {};
var LEFT = 74; //j
var RIGHT = 76; //l
var UP = 73; //i
var DOWN = 75; //k
var ON = "ON";
var OFF = "OFF";
//var SERVER_URL = "http://" + document.URL.split("/")[2] + "/car_srv.php";
var websocket = null;

function wsConnect(){
	if(websocket != null){
		websocket.close();
	}
	else{
		var serverURL = "ws://192.168.1.104:12345";
		websocket = new WebSocket(serverURL);
		
		websocket.onopen = function(evt){
			$("button#wsconnect").text("Disconnect");
			websocket.send("client:" + $("#cars_list option:selected").text());
			//$("#camera").attr("src", "http://" + $("#cars_list option:selected").val() + ":80/file.mjpg");
		};
		websocket.onclose = function(evt){
			$("button#wsconnect").text("Connect");
			websocket = null;
			$("#camera").attr("src", "");
		};
		websocket.onmessage = function(evt){
			if(evt.data == "ping"){
				websocket.send("pong");
			}
			console.log(evt.data);
		};
		websocket.onerror = function(evt){
			console.log(evt);
		};
	}
}

function sendState(){
	if(websocket == null) return;
	
	var timestamp = (new Date()).getTime();
	var left = (keysdown[LEFT] === true) ? ON : OFF;
	var right = (keysdown[RIGHT] === true) ? ON : OFF;
	var up = (keysdown[UP] === true) ? ON : OFF;
	var down = (keysdown[DOWN] === true) ? ON : OFF;
	
	var cmd = "?up=" + up + "&down=" + down + "&left=" + left + "&right=" + right + "&time=" + timestamp;
	websocket.send(cmd);
}

function keypressHandle(e){
	if(e.type == "keydown"){
		if(!keysdown[e.keyCode]){
			keysdown[e.keyCode] = true;
			sendState();
		}
	}
	else if(e.type == "keyup"){
		keysdown[e.keyCode] = false;
		sendState();
	}
	else console.error(e);
}

$(document).ready(function() {
	$(window).keydown(keypressHandle).keyup(keypressHandle);
	$("button#wsconnect").click(wsConnect);
});