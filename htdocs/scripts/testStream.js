var websocket = null;

var prevTime = 0;
var cnt = 0;
var sum = 0;

function wsConnect(){
	if(websocket != null){
		websocket.close();
	}
	else{
		var carURL = "ws://192.168.1.111:12345";
		websocket = new WebSocket(carURL);
		
		websocket.onopen = function(evt){
			prevTime = (new Date()).getTime();
		};
		
		websocket.onclose = function(evt){
			websocket = null;
			console.log(sum / cnt);
		};

		websocket.onmessage = function(evt){
			if(evt.data instanceof Blob){
				console.log((new Date()).getTime() / 1000);
				var curr = (new Date()).getTime();
				var delay = curr - prevTime;
				prevTime = curr;
				//console.log(delay);
				cnt++;
				sum += delay;
				
				curr = (new Date()).getTime()
				//var ctx = $("#canvas")[0].getContext("2d");
				//evt.data.type = "image/jpeg";
				$("#d").attr("src", URL.createObjectURL(evt.data));
				//console.log("draw: " + ((new Date()).getTime() - curr));
				
				/*var image = new Image();
				curr = (new Date()).getTime()
				image.src = URL.createObjectURL(evt.data);
				console.log("draw: " + ((new Date()).getTime() - curr));
				image.onload = function(){
					ctx.drawImage(image, 0, 0, 400, 300);
					//console.log("draw: " + ((new Date()).getTime() - curr));
				}*/
			}
		};
		websocket.onerror = function(evt){
			console.log(evt);
		};
	}
}

$(document).ready(function() {
	wsConnect();
});