var Connect = require("connect");
var ServeStatic = require("serve-static");
var Logging = require("morgan");
var WebSocketServer = require('ws').Server;
var QueryString = require("querystring");

//app is http server that serves static files in /public folder
var app = Connect();
app.use(Logging("combined")); //turn off logging after 
app.use("/cars_list", function(req, res, next){
	res.writeHead(200, {"Content-Type": "application/json"});
	res.end(JSON.stringify(Object.keys(cars)));
});
app.use(ServeStatic(__dirname + "/public"));
app.listen(80);

var CAR_SECRET = 133780085; //car token (shared secret)
var cars = {};

//wss is websocket server
var wss = new WebSocketServer({port: 4113});
wss.on("connection", function(ws){
	ws.on("message", function(message, flags){
		console.log("Message: " + message);
		if(ws.carWS === undefined){
			try{
				var query = QueryString.parse(message);
				var token = parseInt(query.token);
				
				if(token == CAR_SECRET){
					console.log("\nCar token accepted: " + query.name + "\n");
					cars[query.name] = ws;
					ws.name = query.name;
				}
				else if(token > 0 && token < 1000){ //token validation
					console.log("\nClient token " + token + " accepted");
					console.log("Want connection with " + query.name + "\n");
					if(cars[query.name] === undefined)
						throw "car offline";
					else if(cars[query.name].clientWS !== undefined)
						throw "car already connected with some client";
					else{
						ws.carWS = cars[query.name];
						ws.carWS.clientWS = ws;
					}
				}
				else{
					throw "invalid token";
				}
			}
			catch(error){
				ws.close(1000, error);
			}
		}
		else{
			ws.carWS.send(message);
		}
    });
	
	ws.on("close", function(code, message){
		console.log("Disconnect with code: " + code + " and message: " + message);
		if(ws.clientWS !== undefined){
			delete cars[ws.name];
			ws.clientWS.close(1000, "car went offline");
		}
		else if(ws.carWS !== undefined){
			delete ws.carWS.clientWS;
		}
	});
	
	ws.on("error", function(error){
		console.log("ERROR: " + error);
	});
});

console.log("Server running");