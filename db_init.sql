DROP USER IF EXISTS 'whatabook_user'@'localhost';


-- create pysports_user and grant them all privileges to the pysports database 
CREATE USER 'whatabook_user'@'localhost' IDENTIFIED WITH mysql_native_password BY 'MySQL8IsGreat!';

-- grant all privileges to the pysports database to user pysports_user on localhost 
GRANT ALL PRIVILEGES ON whatabook.* TO'whatabook_user'@'localhost';

DROP TABLE IF EXISTS wishlist;
DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS book;
DROP TABLE IF EXISTS store;

CREATE TABLE user (
	user_id		INT		NOT NULL	AUTO_INCREMENT,
	first_name	VARCHAR(75)	NOT NULL,
	last_name	VARCHAR(75)	NOT NULL,
	PRIMARY KEY(user_id)
);

CREATE TABLE book (
	book_id		INT		NOT NULL	AUTO_INCREMENT,
	book_name	VARCHAR(200)	NOT NULL,
	details		VARCHAR(500),
	author		VARCHAR(200)	NOT NULL,
	PRIMARY KEY(book_id)
);

CREATE TABLE store (
	store_id	INT		NOT NULL,
	locale		VARCHAR(500)	NOT NULL,
	PRIMARY KEY(store_id)
);

CREATE TABLE wishlist (
	wishlist_id	INT		NOT NULL	AUTO_INCREMENT,
	user_id		INT		NOT NULL,
	book_id		INT		NOT NULL,
	PRIMARY KEY(wishlist_id),
	FOREIGN KEY(user_id)
		REFERENCES user(user_id),
	FOREIGN KEY(book_id)
		REFERENCES book(book_id)
);

INSERT INTO store(store_id, locale)
	VALUES(001, 'DALLAS');

INSERT INTO book(book_name, details, author)
	VALUES('The Book and the Reader', 'First in the Book franchise', 'Vin Diesel');

INSERT INTO book(book_name, details, author)
	VALUES('2 Book 2 Reader', 'Powerhouse sequel', 'Vin Diesel');

INSERT INTO book(book_name, author)
	VALUES('The Book and the Reader: Tokyo Fable', 'Vin Diesel');

INSERT INTO book(book_name, author)
	VALUES('Book & Reader', 'Vin Diesel');

INSERT INTO book(book_name, author)
	VALUES('Book 5', 'Dominic Toretto');

INSERT INTO book(book_name, author)
	VALUES('Book & Reader 6', 'Dominic Toretto');

INSERT INTO book(book_name, author)
	VALUES('Reader 7', 'Dominic Toretto');

INSERT INTO book(book_name, author)
	VALUES('The Fate of the Reader', 'Dominic Toretto');

INSERT INTO book(book_name, author)
	VALUES('B9', 'Dwayne Johnson');

INSERT INTO user(first_name, last_name)
	VALUES ('Vin', 'Diesel');

INSERT INTO user(first_name, last_name)
	VALUES ('Dwayne', 'Johnson');
    
INSERT INTO user(first_name, last_name)
	VALUES ('Paul', 'Walker');

INSERT INTO wishlist(user_id, book_id)
	VALUES(1, 1);

INSERT INTO wishlist(user_id, book_id)
	VALUES(2, 2);

INSERT INTO wishlist(user_id, book_id)
	VALUES(3, 5);
