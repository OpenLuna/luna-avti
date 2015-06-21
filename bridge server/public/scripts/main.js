var LEFT = 74; //j
var RIGHT = 76; //l
var UP = 73; //i
var DOWN = 75; //k
var ON = "ON";
var OFF = "OFF";
var WS_SERVER = "ws://" + window.location.href.split("/")[2].split(":")[0] + ":4113/";

var keysdown = {};
var websocket = null;

function wsConnection(){
	if(websocket != null){
		websocket.close();
	}
	else{
		var query = "token=123&name=RangeRover";
		websocket = new WebSocket(WS_SERVER);
		
		websocket.onopen = function(evt){
			$("button#ws_connect").text("Disconnect");
			//websocket.send(query);
			websocket.send("123");
			//$("#camera").attr("src", "http://" + $("#cars_list option:selected").val() + ":80/file.mjpg");
		};
		
		websocket.onclose = function(evt){
			$("button#ws_connect").text("Connect");
			$("#camera").attr("src", "");
			websocket = null;
		};
		
		websocket.onmessage = function(evt){
			console.log(evt.data);
		};
		
		websocket.onerror = function(evt){
			console.log(evt);
		};
	}
}

function sendState(){
	if(websocket != null){
		var timestamp = (new Date()).getTime();
		var left = (keysdown[LEFT] === true) ? ON : OFF;
		var right = (keysdown[RIGHT] === true) ? ON : OFF;
		var up = (keysdown[UP] === true) ? ON : OFF;
		var down = (keysdown[DOWN] === true) ? ON : OFF;
		
		var cmd = "?up=" + up + "&down=" + down + "&left=" + left + "&right=" + right + "&time=" + timestamp;
		websocket.send(cmd);
	}
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
	$("button#ws_connect").click(wsConnection);
});