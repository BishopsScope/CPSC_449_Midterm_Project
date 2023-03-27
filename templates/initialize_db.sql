CREATE DATABASE IF NOT EXISTS 449_db;

USE 449_db;

CREATE TABLE IF NOT EXISTS accounts
(
    id INT(11) NOT NULL AUTO_INCREMENT,
    username VARCHAR(50) NOT NULL,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(100) NOT NULL,
    organisation VARCHAR(100) NOT NULL,
    address VARCHAR(100) NOT NULL,
    city VARCHAR(100) NOT NULL,
    state VARCHAR(100) NOT NULL,
    country VARCHAR(100) NOT NULL,
    postalcode VARCHAR(100) NOT NULL,

    PRIMARY KEY (id)

);