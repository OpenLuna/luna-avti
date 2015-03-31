var keysdown = {};
var LEFT = 74; //j
var RIGHT = 76; //l
var UP = 73; //i
var DOWN = 75; //k
var ON = "ON";
var OFF = "OFF";
var URL = "http://" + document.URL.split("/")[2] + "/car_srv.php";

var timerLog = [];

function buttonClick(){
	console.log(timerLog);
	$.redirect(	"http://" + document.URL.split("/")[2] + '/nd.php', 
			{id: $( "#cars_list" ).val(), 
			data: timerLog.join("\n")});
}

var sendState = function() {
	var left = (keysdown[LEFT] === true) ? ON : OFF;
	var right = (keysdown[RIGHT] === true) ? ON : OFF;
	var up = (keysdown[UP] === true) ? ON : OFF;
	var down = (keysdown[DOWN] === true) ? ON : OFF;
	
	var timestamp = (new Date()).getTime();
	
	$.ajax({
		url: URL,
		data: {
			left: left,
			right: right,
			up: up,
			down: down,
			id: $( "#cars_list" ).val(),
			time: timestamp
		},
		success: function(data) {
			$( "#ajax-result" ).text(data);
			var r = $( "#cars_list option:selected" ).text() + "," + timestamp + ",client," + (((new Date()).getTime() - timestamp) / 1000);
			timerLog.push(r);
		}
	});
}

var handledown = function(e) {
	//console.log(e);
	if (keysdown[e.which] ==  false || (typeof keysdown[e.which] === "undefined")) {
		keysdown[e.which] = true;
		switch (e.which) {
			case UP:
				sendState();
				$("#buttonUp").css({backgroundColor: "green"});
				break;
			case LEFT:
				sendState();
				$("#buttonLeft").css({backgroundColor: "green"});
				break;
			case DOWN:
				sendState();
				$("#buttonDown").css({backgroundColor: "green"});
				break;
			case RIGHT:
				sendState();
				$("#buttonRight").css({backgroundColor: "green"});
				break;
		}
	}
}

var handleup = function(e) {
	//console.log(e);
	keysdown[e.which] = false;
	switch (e.which) {
		case UP:
			sendState();
			$("#buttonUp").css({backgroundColor: "lightblue"});
			break;
		case LEFT:
			sendState();
			$("#buttonLeft").css({backgroundColor: "lightblue"});
			break;
		case DOWN:
			sendState();
			$("#buttonDown").css({backgroundColor: "lightblue"});
			break;
		case RIGHT:
			sendState();
			$("#buttonRight").css({backgroundColor: "lightblue"});
			break;
	}
}

$(document).ready(function() {
	// send event on keypress
	$(window).keydown(handledown).keyup(handleup);
	$("button#nd").click(buttonClick);
});