var connect = require("connect"),
	app = connect();
var serveStatic = require("serve-static");
var logging = require("morgan");

app.use(logging("combined"));
app.use(serveStatic(__dirname + "/public"));
app.listen(80);
console.log("Server running");