var socket = io(":" + location.port + "/cart");

// get cart element
var $cart = $('#cart');

// cart items dictionary
var cart = {};

// if items are already in the cart
// add them to the cart items dictionary
$(".item").each(function() {
	// get each item
	$item = $(this);
	// make a dict
	item = {
		"index": $item.attr("id"),
		"name": $item.children("h2").text(),
		"description": $item.children("p").text(),
		"cost": $item.children("h3").text()
	};
	// add it to the cart
	cart[item.index] = item;
	// allow selecting
	$("#"+item.index).on('click touch', function() {
			$(this).toggleClass("remove");
	});

})


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

		console.log(item.index)
		console.log(cart)
		console.log(item.index in cart)

		if (!(item.index in cart)) {
			// update to the ui
			$cart.append(
				"<div class=\"item\" id=\"" + item.index + "\">"
				+ "<h2>" + item.name + "</h2>"
				+ "<p>" + item.description + "</p>"
				+ "<h3 class=\"ui\">" + item.cost + "</h3>" +
				"</div>"
			)

			// allow selecting
			$("#"+item.index).on('click touch', function() {
			    $(this).toggleClass("remove");
			});

			// add to cart items dictionary
			cart[item.index] = item
			console.log(item);
		} else {
			console.log("duplicate item")
		}
});

function remove() {
	$remove = $(".item.remove");
	$remove.each(function () {
		delete cart[$(this).attr("id")];
		$(this).remove();
	});
}

// simulate adding an item
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
	window.location.href = 'http://' + document.domain + ':' + location.port + "/checkout";
}
