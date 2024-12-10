CREATE DATABASE IF NOT EXISTS hotel_management;

USE hotel_management;

CREATE TABLE users (
    uid INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    username VARCHAR(100) UNIQUE,
    password VARCHAR(100),
    phone VARCHAR(15),
    address VARCHAR(255),
    email VARCHAR(100)
);

CREATE TABLE hotels (
    hid INT AUTO_INCREMENT PRIMARY KEY,
    hname VARCHAR(100),
    haddress VARCHAR(255),
    star INT,
    rating FLOAT
);

CREATE TABLE rooms (
    hid INT NOT NULL, 
    total_rooms INT NOT NULL, 
    available INT NOT NULL,    
    price_per_room FLOAT NOT NULL, 
    PRIMARY KEY (hid)  
);

CREATE TABLE bookings (
    booking_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    hotel_id INT,
    room_count INT,
    check_in_date DATE,
    check_out_date DATE,
    FOREIGN KEY (user_id) REFERENCES users(uid),
    FOREIGN KEY (hotel_id) REFERENCES hotels(hid)
);
