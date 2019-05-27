var socket = io();

// get cart element
var $cart = $('#cart');

// cart items dictionary
var cart = {}

// tutorial toggle
var tutorial = true;

// connect to the websocket and send to console
socket.on('connect', function() {
	console.log('websocket connected!');
	console.log(socket.id);
});

// send data over `server request` channel
socket.emit('cart_request', {msg: 'cart_request'});

// receive data on `cart_response` channel
socket.on('cart_response', function(item) {
		if (tutorial) {
			$('#tutorial').remove();
			tutorial = false;
		}
		// update to the ui
		$cart.append(
			"<div class=\"item\" id=\"" + item.index + "\">"
			+ "<h2>" + item.name + "</h2>"
			+ "<p>" + item.description + "</p>"
			+ "<h3 class=\"ui\">" + item.cost + "</h3>" +
			"</div>"
		)

		// allow selecting
		// $("#"+item.index).on('click touch', function() {
		// 	$(this).toggleClass("remove");
		// });
        // allow selecting
        $("#"+item.index).on('click touch', function() {
            $(this).toggleClass("remove");
        });


		// add to cart items dictionary
		cart[item.index] = item
		console.log(item);
});

function remove() {
	$remove = $(".item.remove");
	$remove.each(function () {
		delete cart[$(this).attr("id")];
		$(this).remove();
	});
}

// emulate adding an item
var index = 1;
function sim_add() {
	if (tutorial) {
		$('#tutorial').remove();
		tutorial = false;
	}

	// update to the ui
	$cart.append(
		"<div class=\"item\" id=\"" + index + "\">"
		+ "<h2>Item</h2>"
		+ "<p>Description</p>"
		+ "<h3 class=\"ui\">Cost</h3>" +
		"</div>"
	)

	// allow selecting
	$("#"+index).on('click touch', function() {
		$(this).toggleClass("remove");
	});

	// add to cart items dictionary
	cart[index] = "test"
	console.log(index);
	index++;
}
// send data over `server request` channel
function checkout() {
	socket.emit('checkout_request', {data: cart});
	console.log("boop")
	var locket = io.connect("http://localhost:5000", {resource: '/socket.io', 'force new connection': true});
	// connect to the websocket and send to console
	locket.on('connect', function() {
		console.log('weblocket connected!');
		console.log(locket.id);
	});

	// receive data on `checkout_response` channel
	locket.on('checkout_response', function(payload) {
			// FIXME ui this stuff
			console.log("hello")
			console.log(payload);
	});
	// window.location.href = 'http://' + document.domain + ':' + location.port + "/checkout";
}
