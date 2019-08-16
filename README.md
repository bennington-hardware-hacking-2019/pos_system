# Automated Point of Sale System using NFC

![](demo.gif)

## Purpose

Our goal is to develop an automated point of sale system using near field communications for the Bennington College campus thrift store (TAPA).
We hope that this POS system will help re-establish TAPA by easing the burden of managing inventory and potentially eliminating the expense of employing cashiers.

## High-level architecture

![](architecture.jpg)

- NFC Reader (ISO Format): Read tags.
- NFC Reader (HID Format): Read Bennington IDs.
- Controller: Runs the Backend and User Interface.
- Monitor: 7” touch screen with stand and mount for Controller.
- Database: Store user information, inventory items and transaction details.
- Backend: Prepare transactions, validate transactions using Stripe/Venmo API, update Controller.
- User Interface: A locally hosted web interface for buyers to view, manage, and checkout items in the Cart. Also an admin interface for managing inventory

For more details, please visit the [design
doc](https://docs.google.com/document/d/1uPikHsPxjA35MsOq9hkEmXJNQbgH-Svp_8UPdOPB1fI/edit?usp=sharing).

## Sample Flow

Point of Sale
- Alex taps thrift store items on the NFC reader to add items to the cart
- They can remove items from their cart on the touch screen
- Once they are done they tap their Bennington ID Card to checkout
- The screen will notify that a payment link is sent to the student email
- Now Alex is ready to make their purchase

Administration
- Blake taps the Admin Login button on the touch screen and enters the pin
- Blake can then manage the inventory on the touch screen

## Installing

To install necessary development tools:
```
make init
```

## Using

First,
```
make db-setup && make run
```

Second, access
```
http://127.0.0.1:5000
```

## Developing

To setup postgres with pre-populated data. Used for initial setup and testing
mostly.
```
make db-setup
```

To run test
```
make test
```
