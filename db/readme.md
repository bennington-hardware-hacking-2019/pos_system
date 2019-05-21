# db component

## API

> TODO

## Using

> TODO

## Developing

To install necessary development tools:
```
make init
```

To setup postgres with pre-populated data (mainly used for testing):
```
make db-setup
```
> Use `make run` to simulate a simple flow.

To run test
```
make test
```
## Schema

The [schema file](schema.sql) combined with the [constraint file](constraint.sql) contains the SQL Schema of our database. For convenience this schema is included below:

Schema | Name  | Type  | Owner  
--------|-------|-------|--------
public | admin | table | julian
public | buyer | table | julian
public | item  | table | julian
public | sale  | table | julian
public | stock | table | julian
