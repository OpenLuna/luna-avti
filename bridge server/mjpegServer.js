/*var WebSocketServer = require('ws').Server;
var wss = new WebSocketServer({port: 4113});
console.log("WS server opened");

wss.on('connection', function(ws) {
    ws.on('message', function(message) {
		console.log(message);
    });
});*/
var clientResponse = null;
var http = require('http');
http.createServer(function (req, res) {
	if(req.url == "/video.mjpg"){
		console.log("Client saved");
		clientResponse = res;
		res.writeHead(200, {'Content-Type': 'multipart/x-mixed-replace; boundary=--jpgboundary'});
	}
	else{
		var i = 0;
		req.on('data', function(chunk) {
			//l = chunk[3] + 256 * chunk[2] + 65536 * chunk[1] + 16777216 * chunk[0];
			//console.log(chunk[0] + " " + chunk[1] + " " + chunk[2] + " " + chunk[3] + " " +l);
			clientResponse.write(chunk);
			console.log(i);
			i++;
		});
	}
}).listen(4113);
console.log('Server running');
