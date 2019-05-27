var socket = io.connect('http://' + document.domain + ':' + location.port);

// on checkout_response -> update ui

// get cart element by id
var $cart = $('#cart');

// dictionary to hold cart items
var cart = {}

// verify our websocket connection is established
socket.on('connect', function() { console.log('websocket connected!'); });

// send data over `server request` channel
socket.emit('sale_request', {msg: 'stage_sale'});

function remove() {
	$cart.append("<div class=\"item\"><h2><b>Item</b></h2><p>"+Math.random().toString(36)+"</p><h3 class=\"ui\">Cost</h3></div>")
}
// receive data on `add_response` channel
socket.on('add_to_cart_response', function(item) {
		// update to the ui
		$cart.append('<div class="item blue">' + item.name + ' - ' + item.cost + '</div>');

		// add to checkout dictionary
		checkout_payload[item.name] = item.cost
		console.log(item);
});

// send data over `server request` channel
function checkout() {
		socket.emit('checkout_request', {data: checkout_payload});
}

// receive data on `pay_response` channel
socket.on('pay_response', function(payload) {
		// FIXME ui this stuff
		$checkout.append('<br>');
		$checkout.append('<div class="ui brown">' + payload.msg + '</div>');
		console.log(payload);
});
