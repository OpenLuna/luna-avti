var clientResponse = null;
var http = require('http');
var url = require("url");
http.createServer(function (req, res) {
	if(req.url == "/stream.mjpg"){
		console.log("Client saved");
		clientResponse = res;
		res.writeHead(200, {'Content-Type': 'multipart/x-mixed-replace; boundary=--jpgboundary'});
		req.on("close", function(){
			console.log("end connection");
			clientResponse = null;
		});
	}
	else{
		console.log(url.parse(req.url, true));
		var i = 0;
		req.on('data', function(chunk) {
			if(clientResponse != null){
				clientResponse.write(chunk);
			}
		});
	}
}).listen(4114);
console.log('Server running');
