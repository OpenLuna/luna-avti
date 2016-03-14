var Connect = require("connect");
var ServeStatic = require("serve-static");
var Logging = require("morgan");
var WebSocketServer = require('ws').Server;
var QueryString = require("querystring");
var URL = require("url");
var http = require("http");

//app is http server that serves static files in /public folder
var app = Connect();
//app.use(Logging("combined")); //turn off logging after 
app.use("/cars_list", function (req, res, next) {
    res.writeHead(200, {
        "Content-Type": "application/json"
    });
    res.end(JSON.stringify(Object.keys(carsWS)));
});
app.use(ServeStatic(__dirname + "/public"));
app.listen(8080);

var CAR_SECRET = 133780085; //car token (shared secret)
var carsWS = {}; //websocket connections of cars
var carsVideo = {}; //stream redirections for cars

function checkSecret(secret, callback) {
    var postdata = QueryString.stringify({
        'secret': secret
    });

    var options = {
        'hostname': 'pelji.se',
        'port': '80',
        'path': '/check',
        'method': 'POST',
        'headers': {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Content-Length': postdata.length
        }
    }

    var req = http.request(options, function (res) {
        res.setEncoding('utf8');

        var rdata = '';

        res.on('data', function (chunk) {

            rdata = rdata + chunk;

        });

        res.on('end', function () {

            return callback(rdata);

        })
    });

    req.on('error', function (e) {
        console.log('problem with request: ' + e.message);
    });

    // write data to request body
    req.write(postdata);
    req.end();
}

function updateWaitList(callback) {
    var options = {
        'hostname': 'pelji.se',
        'port': '80',
        'path': '/updateWaitList',
        'method': 'GET',
        'headers': {
            'Content-Type': 'application/json',
        }
    }

    var req = http.request(options, function (res) {
        res.setEncoding('utf8');

        var rdata = '';

        res.on('data', function (chunk) {

            rdata = rdata + chunk;

        });

        res.on('end', function () {

            return callback(rdata);

        })
    });

    req.on('error', function (e) {
        console.log('problem with updateWaitLis request: ' + e.message);
    });

    req.end();
}

//streamApp is http server that redirects mjpeg streams
//var streamApp = Connect();
//streamApp.use("/streamreg", function (req, res, next) {
//    query = URL.parse(req.url, true).query;
//    if (query.token == CAR_SECRET) {
//        console.log("[ST] Video stream from >>" + query.name + "<< registered");
//        carsVideo[query.name] = req;
//
//        /*req.on("close", function(){
//        	console.log("Video stream from " + query.name + " went offline");
//        	delete carsVideo[query.name];
//        });*/
//    } else {
//        res.writeHead(404);
//        res.end("wrong token for video stream registration");
//    }
//});
//streamApp.use(function (req, res, next) { //video stream to client
//    var query = URL.parse(req.url, true).query;
//    res.writeHead(200, {
//        'Content-Type': 'multipart/x-mixed-replace; boundary=--jpgboundary'
//    });
//
//    if (carsVideo[query.name] !== undefined) {
//        console.log("[ST] Client connected to video stream of >>" + query.name + "<<");
//        carsVideo[query.name].pipe(res);
//
//        req.on("close", function () {
//            console.log("[ST] Client disconnected from video stream of >>" + query.name + "<<");
//            if (carsVideo[query.name] !== undefined)
//                carsVideo[query.name].unpipe(res);
//        });
//    } else {
//        res.writeHead(404);
//        res.end("video stream is not online");
//    }
//});
//var server = http.createServer(streamApp).listen(4114);
//server.timeout = 0;

var secret;
var secretchecker;
//wss is websocket server
var wss = new WebSocketServer({
    port: 4113
});
wss.on("connection", function (ws) {
    ws.on("message", function (message, flags) {
        //console.log("Message: " + message);
        if (ws.carWS === undefined) {
            try {
                var query = QueryString.parse(message);
                var token = parseInt(query.token);

                //car token
                if (token == CAR_SECRET) {
                    console.log("[WS] Car >>" + query.name + "<< advertised");
                    ws.type = "car";
                    ws.name = query.name;
                    carsWS[query.name] = ws;
                } else if (token > 0 && token < 1000) { //client token validation
                    ws.type = "client";
                    ws.token = token;
                    if (carsWS[query.name] === undefined)
                        throw "car offline";
                    else if (carsWS[query.name].clientWS !== undefined)
                        throw "car busy";
                    else { //accept connection

                        secret = query.secret;

                        checkSecret(secret, function (data) {
                            if (data == 0) {
                                clearInterval(secretchecker);
                                if (carsWS['Scorpion'].clientWS !== undefined) {
                                    carsWS['Scorpion'].clientWS.close(1000, 'wrong secret'); // TODO Scorpion hack
                                }
                            } else {
                                console.log('secret ok');

                                secretchecker = setInterval(function () {
                                    checkSecret(secret, function (data, name) {
                                        if (data == 0) {
                                            console.log('wrong secret');
                                            var cmd = "up=OFF&down=OFF&left=OFF&right=OFF";
                                            ws.carWS.send(cmd);

                                            if (carsWS['Scorpion'].clientWS !== undefined) {
                                                carsWS['Scorpion'].clientWS.close(1000, 'wrong secret'); // TODO Scorpion hack
                                            }
                                        } else {
                                            console.log('secret ok');
                                        }
                                    });
                                }, 1000);

                            }
                        });

                        console.log("[WS] Client (" + token + ") connected with car >>" + query.name + "<<");
                        ws.carWS = carsWS[query.name]; //connect client websocket with car websocket
                        ws.carWS.clientWS = ws; //connect car websocket with client websocket

                        setInterval(function () {
                            updateWaitList(function (data, name) {
                                console.log("update wait list")
                            });
                        }, 5000);
                        
                    }
                } else {
                    throw "invalid token";
                }
            } catch (error) {
                ws.close(1000, error);
            }
        } else { //client sends message. redirect to car
            try {

                //                secret = query.secret;

                ws.carWS.send(message);

                //                checkSecret(secret, function (data) {
                //                    if (data == 0) {
                //                        console.log(secret);
                //                        if (ws.clientWS != undefined) {
                //                            ws.clientWS.close(1000, "wrong secret");
                //                        }
                //                    } else {
                //                        console.log('secret ok');
                //
                //                    }
                //                });

            } catch (e) {
                console.log("[WS] " + e);
                ws.close();
            }
        }
    });

    ws.on("close", function (code, message) {
        if (ws.type == "car") {
            console.log("[WS] Car >>" + ws.name + "<< disconnected (" + code + ")");
        } else if (ws.type == "client") {
            if (ws.carWS !== undefined) {
                var cmd = "up=OFF&down=OFF&left=OFF&right=OFF";
                ws.carWS.send(cmd);
            }
            console.log("[WS] Client (" + ws.token + ") disconnected (" + code + ")" + ((message) ? ": " + message : ""));
        }

        if (ws.type == "car" && ws == carsWS[ws.name]) {
            delete carsWS[ws.name];
            if (ws.clientWS !== undefined) { //closing connection with car that is connected with client
                ws.clientWS.close(1000, "car went offline"); //close client and send reason
            }
        } else if (ws.type == "client") {
            if (ws.carWS !== undefined) { //closing connection with client
                delete ws.carWS.clientWS;
            }
        }

        clearInterval(secretchecker);
    });

    ws.on("error", function (error) {
        console.log("[WS] ERROR: " + error);
    });
});

console.log("SERVER RUNNING\n");