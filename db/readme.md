# db component

## API

> TODO

## Using

> TODO

## Developing

> TODO

## Schema

The [schema file](schema.sql) combined with the [constraint file](constraint.sql) contains the SQL Schema of our database. For convenience this schema is included below:

Schema | Name  | Type  | Owner  
--------|-------|-------|--------
public | [admin](#admin) | table | postgres
public | [buyer](#buyer) | table | postgres
public | [item](#item)  | table | postgres
public | [sale](#sale)  | table | postgres
public | [stock](#stock) | table | postgres

### admin

Column     |  Type   | Collation | Nullable |               Default                | Storage | Stats target | Description
---------------|---------|-----------|----------|--------------------------------------|---------|--------------|-------------
index         | integer |           | not null | nextval('admin_index_seq'::regclass) | plain   |              |
bennington_id | integer |           | not null |                                      | plain   |              |
super_admin   | boolean |           |          |                                      | plain   |              |

Indexes:
- "admin_pkey" PRIMARY KEY, btree (bennington_id)
- "admin_index_key" UNIQUE CONSTRAINT, btree (index)

Foreign-key constraints:
- "buyers_are_admins" FOREIGN KEY (bennington_id) REFERENCES buyer(bennington_id) ON UPDATE CASCADE ON DELETE CASCADE

[Schema overview](#schema)

### buyer

Column     |          Type          | Collation | Nullable |               Default                | Storage  | Stats target | Description
---------------|------------------------|-----------|----------|--------------------------------------|----------|--------------|-------------
index         | integer                |           | not null | nextval('buyer_index_seq'::regclass) | plain    |              |
bennington_id | integer                |           | not null |                                      | plain    |              |
card          | integer                |           | not null |                                      | plain    |              |
name          | character varying(255) |           | not null |                                      | extended |              |
email         | character varying(255) |           | not null |                                      | extended |              |

Indexes:
- "buyer_pkey" PRIMARY KEY, btree (bennington_id)
- "buyer_card_key" UNIQUE CONSTRAINT, btree (card)
- "buyer_email_key" UNIQUE CONSTRAINT, btree (email)
- "buyer_index_key" UNIQUE CONSTRAINT, btree (index)

Referenced by:
- TABLE "admin" CONSTRAINT "buyers_are_admins" FOREIGN KEY (bennington_id) REFERENCES buyer(bennington_id) ON UPDATE CASCADE ON DELETE CASCADE

[Schema overview](#schema)

### item

Column    |            Type             | Collation | Nullable |               Default               | Storage  | Stats target | Description
-------------|-----------------------------|-----------|----------|-------------------------------------|----------|--------------|-------------
index       | integer                     |           | not null | nextval('item_index_seq'::regclass) | plain    |              |
tag         | integer[]                   |           | not null |                                     | extended |              |
item        | character varying(255)      |           | not null |                                     | extended |              |
description | character varying(255)      |           |          |                                     | extended |              |
cost        | money                       |           | not null |                                     | plain    |              |
date_added  | timestamp without time zone |           | not null | CURRENT_TIMESTAMP                   | plain    |              |
sale_index  | integer                     |           |          |                                     | plain    |              |

Indexes:
- "item_pkey" PRIMARY KEY, btree (tag)
- "item_index_key" UNIQUE CONSTRAINT, btree (index)

Foreign-key constraints:
- "sales_have_items" FOREIGN KEY (sale_index) REFERENCES sale(index) ON UPDATE CASCADE ON DELETE SET NULL

Referenced by:
- TABLE "stock" CONSTRAINT "items_in_stock" FOREIGN KEY (item_index) REFERENCES item(index) ON UPDATE CASCADE ON DELETE CASCADE

[Schema overview](#schema)

### sale

Column     |            Type             | Collation | Nullable |               Default               | Storage | Stats target | Description
---------------|-----------------------------|-----------|----------|-------------------------------------|---------|--------------|-------------
index         | integer                     |           | not null | nextval('sale_index_seq'::regclass) | plain   |              |
bennington_id | integer                     |           | not null |                                     | plain   |              |
date_added    | timestamp without time zone |           | not null | CURRENT_TIMESTAMP                   | plain   |              |
date_paid     | timestamp without time zone |           |          |                                     | plain   |              |

Indexes:
- "sale_pkey" PRIMARY KEY, btree (index)
- "sale_bennington_id_key" UNIQUE CONSTRAINT, btree (bennington_id)

Referenced by:
- TABLE "item" CONSTRAINT "sales_have_items" FOREIGN KEY (sale_index) REFERENCES sale(index) ON UPDATE CASCADE ON DELETE SET NULL

[Schema overview](#schema)

### stock

Column   |  Type   | Collation | Nullable |               Default                | Storage | Stats target | Description
------------|---------|-----------|----------|--------------------------------------|---------|--------------|-------------
index      | integer |           | not null | nextval('stock_index_seq'::regclass) | plain   |              |
item_index | integer |           | not null |                                      | plain   |              |

Indexes:
- "stock_pkey" PRIMARY KEY, btree (index)
- "stock_item_index_key" UNIQUE CONSTRAINT, btree (item_index)

Foreign-key constraints:
- "items_in_stock" FOREIGN KEY (item_index) REFERENCES item(index) ON UPDATE CASCADE ON DELETE CASCADE

[Schema overview](#schema)
