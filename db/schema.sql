/* schema for the tapa database */

CREATE TABLE IF NOT EXISTS account (
  index SERIAL NOT NULL,
  bennington_id INT UNIQUE NOT NULL,
  nfc_card INT UNIQUE NOT NULL,
  name VARCHAR(255) NOT NULL,
  email VARCHAR(255) UNIQUE NOT NULL,
  role VARCHAR(20) NOT NULL,
  PRIMARY KEY (bennington_id));

CREATE TABLE IF NOT EXISTS inventory (
  index SERIAL NOT NULL,
  date_added TIMESTAMP NOT NULL,
  nfc_tag INT UNIQUE NOT NULL,
  item VARCHAR(255) NOT NULL,
  description VARCHAR(255) NULL,
  status VARCHAR(20) NOT NULL,
  price NUMERIC(5,2) NOT NULL,
  PRIMARY KEY (nfc_tag));

CREATE TABLE IF NOT EXISTS transaction (
  index SERIAL NOT NULL,
  transaction_id VARCHAR(36) UNIQUE NOT NULL,
  nfc_tag INT UNIQUE NOT NULL,
  bennington_id INT UNIQUE NOT NULL,
  date_added TIMESTAMP NOT NULL,
  date_paid TIMESTAMP NOT NULL,
  status VARCHAR(20) NOT NULL,
  PRIMARY KEY (transaction_id));
