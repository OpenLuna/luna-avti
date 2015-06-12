var WebSocketServer = require('ws').Server;
var wss = new WebSocketServer({port: 8080});
console.log("WS server opened");

cars = {}

wss.on('connection', function(ws) {
    ws.on('message', function(message) {
		console.log(message);
		if(message[0] != "?"){
			var msg = message.split(":");
			if(msg[0] == "car"){
				cars[msg[1]] = ws;
			}
			else if(msg[0] == "client"){
				ws.carWS = cars[msg[1]];
			}
		}
		else{
			ws.carWS.send(message);
		}
    });
});
