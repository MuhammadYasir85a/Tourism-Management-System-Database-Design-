-- =============================
-- dbDDL.sql
-- Database DDL for Tourism Management System
-- =============================

CREATE DATABASE TMS;
USE TMS;

-- ========== TABLES ==========

-- Admin Table
CREATE TABLE Admin (
    adminID INT PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(60) NOT NULL
);

-- User Table
CREATE TABLE User (
    userID INT PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(60) NOT NULL,
    contactNumber VARCHAR(15) DEFAULT NULL
);

-- Destination Table
CREATE TABLE Destination (
    destinationID INT PRIMARY KEY,
    adminID INT DEFAULT NULL,
    name VARCHAR(50) NOT NULL,
    street VARCHAR(100) NOT NULL,
    city VARCHAR(30)  NOT NULL,
    description TEXT DEFAULT NULL,
    category VARCHAR(100) DEFAULT  NULL,
    image_url VARCHAR(500) DEFAULT NULL,
    FOREIGN KEY (adminID) REFERENCES Admin(adminID) ON DELETE SET NULL
);

-- Favourite Table
CREATE TABLE Favourite (
    destinationID INT NOT NULL,
    userID INT NOT NULL,
    favouriteDate DATE DEFAULT NULL,
    PRIMARY KEY (destinationID, userID),
    FOREIGN KEY (destinationID) REFERENCES Destination(destinationID) ON DELETE CASCADE,
    FOREIGN KEY (userID) REFERENCES User(userID) ON DELETE CASCADE
);

-- Visit Table
CREATE TABLE Visit (
    destinationID INT NOT NULL,
    userID INT NOT NULL,
    visitDate DATE DEFAULT NULL,
    PRIMARY KEY (destinationID, userID),
    FOREIGN KEY (destinationID) REFERENCES Destination(destinationID) ON DELETE CASCADE,
    FOREIGN KEY (userID) REFERENCES User(userID) ON DELETE CASCADE
);

-- Hotel Table
CREATE TABLE Hotel (
    hotelID INT PRIMARY KEY,
    adminID INT DEFAULT NULL,
    name VARCHAR(50) NOT NULL,
    street VARCHAR(100) NOT NULL,
    city VARCHAR(30)  NOT NULL,
    facilities TEXT DEFAULT NULL,
    image_url VARCHAR(500) DEFAULT NULL,
    FOREIGN KEY (adminID) REFERENCES Admin(adminID) ON DELETE SET NULL
);

-- Booking Table
CREATE TABLE Booking (
    bookingID INT PRIMARY KEY,
    userID INT NOT NULL,
    hotelID INT NOT NULL,
    checkInDate DATE NOT NULL,
    checkOutDate DATE NOT NULL,
    roomType VARCHAR(30) DEFAULT NULL,
    cost DECIMAL(8, 2) DEFAULT NULL,
    bookingDate DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (userID) REFERENCES User(userID) ON DELETE CASCADE,
    FOREIGN KEY (hotelID) REFERENCES Hotel(hotelID) ON DELETE CASCADE
);

-- Restaurant Table
CREATE TABLE Restaurant (
    restaurantID INT PRIMARY KEY,
    adminID INT DEFAULT NULL,
    destinationID INT NOT NULL,
    name VARCHAR(50) NOT NULL,
    street VARCHAR(100) NOT NULL,
    city VARCHAR(30) NOT NULL,
    cuisine VARCHAR(30) DEFAULT NULL,
    image_url VARCHAR(500) DEFAULT NULL,
    FOREIGN KEY (adminID) REFERENCES Admin(adminID) ON DELETE SET NULL,
    FOREIGN KEY (destinationID) REFERENCES Destination(destinationID) ON DELETE CASCADE
);

-- Reservation Table
CREATE TABLE Reservation (
    reservationID INT PRIMARY KEY,
    userID INT NOT NULL,
    restaurantID INT NOT NULL,
    reservationDate DATE NOT NULL,
    reservationTime TIME NOT NULL,
    numberOfGuests INT DEFAULT 1 CHECK (numberOfGuests >= 1),
    tableNumber VARCHAR(20) DEFAULT NULL,
    FOREIGN KEY (userID) REFERENCES User(userID) ON DELETE CASCADE,
    FOREIGN KEY (restaurantID) REFERENCES Restaurant(restaurantID) ON DELETE CASCADE
);

-- Transportation Table
CREATE TABLE Transportation (
    transportationID INT PRIMARY KEY,
    destinationID INT NOT NULL,
    adminID INT NOT NULL,
    type VARCHAR(30) DEFAULT NULL,
    provider VARCHAR(50) DEFAULT NULL,
    FOREIGN KEY (destinationID) REFERENCES Destination(destinationID) ON DELETE CASCADE,
    FOREIGN KEY (adminID) REFERENCES Admin(adminID) ON DELETE CASCADE
);

-- Travel Table
CREATE TABLE Travel (
    travelID INT PRIMARY KEY,
    userID INT NOT NULL,
    transportationID INT NOT NULL,
    travelDate DATE NOT NULL,
    departureTime TIME NOT NULL,
    arrivalTime TIME NOT NULL,
    fare DECIMAL(8, 2) NOT NULL,
    departurePoint VARCHAR(50) NOT NULL,
    arrivalPoint VARCHAR(50) NOT NULL,
    FOREIGN KEY (userID) REFERENCES User(userID) ON DELETE CASCADE,
    FOREIGN KEY (transportationID) REFERENCES Transportation(transportationID) ON DELETE CASCADE
);

-- Review Table
CREATE TABLE Review (
    reviewID INT PRIMARY KEY,
    userID INT NOT NULL,
    destinationID INT DEFAULT NULL,
    restaurantID INT DEFAULT NULL,
    transportationID INT DEFAULT NULL,
    hotelID INT DEFAULT NULL,
    rating TINYINT NOT NULL CHECK (rating BETWEEN 1 AND 5),
    comment TEXT DEFAULT NULL,
    reviewType VARCHAR(50) DEFAULT NULL,
    FOREIGN KEY (userID) REFERENCES User(userID) ON DELETE CASCADE,
    FOREIGN KEY (destinationID) REFERENCES Destination(destinationID) ON DELETE SET NULL,
    FOREIGN KEY (restaurantID) REFERENCES Restaurant(restaurantID) ON DELETE SET NULL,
    FOREIGN KEY (transportationID) REFERENCES Transportation(transportationID) ON DELETE SET NULL,
    FOREIGN KEY (hotelID) REFERENCES Hotel(hotelID) ON DELETE SET NULL
);

