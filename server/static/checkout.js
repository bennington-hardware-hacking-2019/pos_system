var socket = io(":" + location.port + "/checkout");

$checkout = $("#checkout-form");

// connect to the websocket and send to console
socket.on('connect', function() {
	console.log('websocket connected!');
	console.log(socket.id);
});

// receive data on `checkout_response` channel
socket.on('checkout_response', function(payload) {
		// FIXME ui this stuff
		console.log(payload);
		$checkout.append("<h4>Please, confirm the information below:</h4>")
		$checkout.append("<input type=\"text\" name=\"name\" value=" + payload["name"] + " disabled>")
		$checkout.append("<input type=\"email\" name=\"email\" value=" + payload["email"] + " disabled>")
		$checkout.append("<input type=\"text\" name=\"card\" value=" + payload["card"] + " disabled>")
		$checkout.append("<input type=\"text\" name=\"tags\" value=" + payload["tags"] + " disabled>")
		$checkout.append("<br>")
		$checkout.append("<button type=\"submit\">Start</button>")
});











