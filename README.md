# Near Field Communications (NFC) based Point of Sale (POS) System
For Bennington College Thrift and Public Apparel (TAPA)

![](demo.gif)

## Purpose

Our goal is to develop an automated point of sale system using near field communications for the Bennington College campus thrift store (TAPA). We hope that this POS system will help re-establish TAPA by easing the burden of managing inventory and potentially eliminating the expense of employing cashiers.

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
