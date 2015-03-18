var keysdown = {};
var LEFT = 74;
var RIGHT = 76;
var UP = 73;
var DOWN = 75;
var ON = "ON";
var OFF = "OFF";
var commandCount = 0;

//var URL = "http://193.2.176.139:80/car_srv.php";
//var URL = "http://192.168.1.147:80/car_srv.php";
var URL = "http://localhost:80/car_srv.php";

var send = function(message) {
	$.ajax({
		url: URL,
		data: {
			command: message,
			id: $("input[name=avtoID]:checked").val(),
			time: commandCount
		},
		success: function(data) {
			$("#ajax-result").text(data);
		}
	});
	commandCount += 1;
}

var sendState = function() {
	var left = (keysdown[LEFT] === true) ? ON : OFF;
	var right = (keysdown[RIGHT] === true) ? ON : OFF;
	var up = (keysdown[UP] === true) ? ON : OFF;
	var down = (keysdown[DOWN] === true) ? ON : OFF;
	
	$.ajax({
		url: URL,
		data: {
			left: left,
			right: right,
			up: up,
			down: down,
			id: $("input[name=avtoID]:checked").val()
		},
		success: function(data) {
			$("#ajax-result").text(data);
		}
	});
}

var handledown = function(e) {
	if (keysdown[e.which] ==  false || (typeof keysdown[e.which] === "undefined")) {
		keysdown[e.which] = true;
		switch (e.which) {
			case 73: // i
				$("#buttonUp").css({backgroundColor: "green"});
				//send("UP");
				sendState();
				break;
			case 74: // j
				$("#buttonLeft").css({backgroundColor: "green"});
				//send("LEFT");
				sendState();
				break;
			case 75: // k
				$("#buttonDown").css({backgroundColor: "green"});
				//send("DOWN");
				sendState();
				break;
			case 76: // l
				$("#buttonRight").css({backgroundColor: "green"});
				//send("RIGHT");
				sendState();
				break;
		}
	}
}

var handleup = function(e) {
	keysdown[e.which] = false;
	switch (e.which) {
		case 73: // i
			$("#buttonUp").css({backgroundColor: "lightblue"});
			//send("UP");
			sendState();
			break;
		case 74: // j
			$("#buttonLeft").css({backgroundColor: "lightblue"});
			//send("LEFT");
			sendState();
			break;
		case 75: // k
			$("#buttonDown").css({backgroundColor: "lightblue"});
			//send("DOWN");
			sendState();
			break;
		case 76: // l
			$("#buttonRight").css({backgroundColor: "lightblue"});
			//send("RIGHT");
			sendState();
			break;
	}
}

$(document).ready(function() {
	// send event on click
	$("td.full").click(function() {
		send($(this).text())
	});

	// send event on keypress
	$(window).keydown(handledown).keyup(handleup);
});