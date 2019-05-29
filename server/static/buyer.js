var socket = io(":" + location.port + "/card");

$card = $("#card");

// connect to the websocket and send to console
socket.on('connect', function() {
	console.log('websocket connected!');
	console.log(socket.id);
});

function card() {
	socket.emit('card_request');

	// receive data on `checkout_response` channel
	socket.on('card_response', function(payload) {
			$card.text("Buyer Carded")
			// FIXME ui this stuff
			console.log(payload);
	});
}
