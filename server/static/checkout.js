var socket = io.connect('http://' + document.domain + ':' + location.port);

// on checkout_response -> update ui
$checkout = $("#checkout")

// receive data on `checkout_response` channel
socket.on('checkout_response', function(payload) {
		// FIXME ui this stuff
		$checkout.append('<div class="ui brown">' + payload.msg + '</div>');
		console.log(payload);
});
