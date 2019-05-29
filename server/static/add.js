var socket = io(":" + location.port + "/tag");

$tag = $("#tag");

// connect to the websocket and send to console
socket.on('connect', function() {
	console.log('websocket connected!');
	console.log(socket.id);
});

function tag() {
	socket.emit('tag_request');

	// receive data on `checkout_response` channel
	socket.on('tag_response', function(payload) {
			$tag.text("Item Tagged")
			// FIXME ui this stuff
			console.log(payload);
	});
}
