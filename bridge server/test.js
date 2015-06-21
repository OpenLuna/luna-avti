var Connect = require("connect");
var ServeStatic = require("serve-static");
var Logging = require("morgan");
var WebSocketServer = require('ws').Server;
var URL = require("url");
var QueryString = require("querystring");

//app is http server that serves static files in /public folder
var app = Connect();
//app.use(Logging("combined")); //turn off logging after dev
app.use(ServeStatic(__dirname + "/public"));
app.listen(80);

var CAR_SECRET = 133780085; //car token (shared secret)
var cars = {};

/*function verifyWS(info, callback){
	var query = URL.parse(info.req.url, true).query;
	var accept = true;
	var message = "";
	
	try{
		var token = parseInt(query.token);
		
		if(token == CAR_SECRET){
			console.log("Car token accepted");
		}
		else if(token > 0 && token < 1000){ //token validation
			console.log("Client token " + token + " accepted");
		}
		else{
			throw "invalid token";
		}
	}
	catch(error){
		accept = false;
		message = error;
	}
	finally{
		callback(accept, 404, message);
	}
}*/

//wss is websocket server
var wss = new WebSocketServer({port: 4113});
wss.on("connection", function(ws){
	ws.on("message", function(message, flags){
		console.log(message);
		if(ws.carWS === undefined){
			try{
				var query = QueryString.parse(message);
				var token = parseInt(query.token);
				
				if(token == CAR_SECRET){
					console.log("Car token accepted: " + query.name);
					cars[query.name] = ws;
				}
				else if(token > 0 && token < 1000){ //token validation
					console.log("Client token " + token + " accepted");
					console.log("Want connection with " + query.name);
				}
				else{
					throw "invalid token";
				}
			}
			catch(error){
				ws.close();
			}
		}
    });
	
	ws.on("close", function(code, message){
		console.log("Disconnect with code: " + code);
	});
	
	ws.on("error", function(error){
		console.log(error);
	});
});

console.log("Server running");