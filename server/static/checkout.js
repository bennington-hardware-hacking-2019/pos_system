var socket = io();

// on checkout_response -> update ui
$checkout = $("#checkout")

// connect to the websocket and send to console
socket.on('connect', function() {
	console.log('websocket connected!');
	// receive data on `checkout_response` channel
	socket.on('checkout_response', function(payload) {
			// FIXME ui this stuff
			console.log("hello")
			$checkout.append('<div class="ui brown">' + payload.msg + '</div>');
			console.log(payload);
	});

});
