var keysdown = {};
var LEFT = 74; //j
var RIGHT = 76; //l
var UP = 73; //i
var DOWN = 75; //k
var ON = "ON";
var OFF = "OFF";
var SERVER_URL = "http://" + document.URL.split("/")[2] + "/car_srv.php";
var websocket = null;

prevTime = 0;
sumTime = 0;
pkgCnt = -1;

function wsConnect(){
	if(websocket != null){
		websocket.close();
	}
	else{
		var carURL = "ws://" + $("#cars_list option:selected").val();
		websocket = new WebSocket(carURL);
		console.log(websocket.binaryType);
		websocket.onopen = function(evt){
			$("button#wsconnect").text("Disconnect");
			sumTime = 0;
			pkgCnt = -1;
		};
		websocket.onclose = function(evt){
			$("button#wsconnect").text("Connect");
			websocket = null;
			console.log("average: " + (sumTime / pkgCnt));
		};
		websocket.onmessage = function(evt){
			startTime = (new Date()).getTime();
			
			if(pkgCnt > -1){
				sumTime += startTime - prevTime;
				console.log(startTime - prevTime);
			}
			pkgCnt++;
			prevTime = startTime;
			
			var ctx = $("#canvas")[0].getContext("2d");
			evt.data.type = "image/jpeg";
			var image = new Image();
			image.src = URL.createObjectURL(evt.data);
			image.onload = function(){
				ctx.drawImage(image, 0, 0, 400, 300);
			}
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