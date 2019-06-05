# pos_system

![](checkout_demo.gif)

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
