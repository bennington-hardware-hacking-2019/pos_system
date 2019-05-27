var socket = io(":" + location.port + "/cart");

$checkout = $("#checkout");

// connect to the websocket and send to console
socket.on('connect', function() {
	console.log('websocket connected!');
	console.log(socket.id);
});

// receive data on `checkout_response` channel
socket.on('cart_response', function(payload) {
		// FIXME ui this stuff
		console.log("hello")
		console.log(payload);
});
