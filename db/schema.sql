/* schema for the tapa database */

CREATE TABLE IF NOT EXISTS buyer (
	index SERIAL NOT NULL,
	bennington_id INT UNIQUE NOT NULL,
	card INT UNIQUE NOT NULL,
	name VARCHAR(255) NOT NULL,
	email VARCHAR(255) UNIQUE NOT NULL,
	PRIMARY KEY (bennington_id));

CREATE TABLE IF NOT EXISTS admin (
	index SERIAL NOT NULL,
	bennington_id INT UNIQUE NOT NULL,
	super_admin BOOLEAN,
	PRIMARY KEY (bennington_id));

CREATE TABLE IF NOT EXISTS item (
	index SERIAL NOT NULL,
	tag INT[] UNIQUE NOT NULL,
	item VARCHAR(255) NOT NULL,
	description VARCHAR(255) NULL,
	cost MONEY NOT NULL,
	date_added TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
	sale_index INT,
	PRIMARY KEY (tag));

-- What if an tag is reused? Or perhaps an item is returned?

CREATE TABLE IF NOT EXISTS stock (
	index SERIAL NOT NULL,
	item_index INT NOT NULL,
	PRIMARY KEY (index));

CREATE TABLE IF NOT EXISTS sale (
	index SERIAL NOT NULL,
	bennington_id INT UNIQUE NOT NULL,
	date_added TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
	date_paid TIMESTAMP,
	PRIMARY KEY (index));
