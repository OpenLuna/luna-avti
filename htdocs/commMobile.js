var SERVER_URL = "http://" + document.URL.split("/")[2] + "/car_srv.php";
var websocket = null;
var state = {up: false, down: false, left:false, right: false};

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

function orientationHandle(e){
	if(websocket == null) return;
	
	//$("#orientout").html(e.alpha + "<br/>" + e.beta + "<br/>" + e.gamma);
	
	var delta = 10;
	var changed = false;
	
	if(e.beta < -delta){
		if(!state.left){
			state.left = true;
			changed = true;
		}
	}
	else if(e.beta > delta){
		if(!state.right){
			state.right = true;
			changed = true;
		}
	}
	else if(state.left || state.right){
		state.left = false;
		state.right = false;
		changed = true;
	}
	
	if(changed){
		var cmd = "?up=" + (state.up ? "ON":"OFF") + "&down=" + (state.down ? "ON":"OFF") + "&left=" + (state.left ? "ON":"OFF") + "&right=" + (state.right ? "ON":"OFF") + "&time=" + ((new Date).getTime());
		websocket.send(cmd);
	}
}

function gas(evt){
	evt.preventDefault();
	if(evt.type == "touchstart" || evt.type == "mousedown"){
		if(evt.target.id == "forward") state.up = true;
		else state.down = true;
	}
	else{
		if(evt.target.id == "forward") state.up = false;
		else state.down = false;
	}
	
	var cmd = "?up=" + (state.up ? "ON":"OFF") + "&down=" + (state.down ? "ON":"OFF") + "&left=" + (state.left ? "ON":"OFF") + "&right=" + (state.right ? "ON":"OFF") + "&time=" + ((new Date).getTime());
	websocket.send(cmd);
}

$(document).ready(function() {
	window.addEventListener("deviceorientation", orientationHandle, false);
	$("button#wsconnect").click(wsConnect);
	$("#forward, #backward").on("touchstart touchend mousedown mouseup", gas);
});