from datetime import datetime, date
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
# Import db directly from app module
import app
db = app.db

class Admin(UserMixin, db.Model):
    __tablename__ = 'admin'
    
    adminID = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(256), nullable=False)
    
    # Relationships
    destinations = db.relationship('Destination', backref='admin', lazy=True)
    hotels = db.relationship('Hotel', backref='admin', lazy=True)
    restaurants = db.relationship('Restaurant', backref='admin', lazy=True)
    transportation = db.relationship('Transportation', backref='admin', lazy=True)
    
    def get_id(self):
        return str(self.adminID)
    
    def set_password(self, password):
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password, password)

class User(UserMixin, db.Model):
    __tablename__ = 'user'
    
    userID = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(256), nullable=False)
    contactNumber = db.Column(db.String(15), nullable=True)
    
    # Relationships with cascade delete
    bookings = db.relationship('Booking', backref='user', lazy=True, cascade='all, delete-orphan')
    reservations = db.relationship('Reservation', backref='user', lazy=True, cascade='all, delete-orphan')
    travels = db.relationship('Travel', backref='user', lazy=True, cascade='all, delete-orphan')
    reviews = db.relationship('Review', backref='user', lazy=True, cascade='all, delete-orphan')
    favourites = db.relationship('Favourite', backref='user', lazy=True, cascade='all, delete-orphan')
    visits = db.relationship('Visit', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def get_id(self):
        return str(self.userID)
    
    def set_password(self, password):
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password, password)

class Destination(db.Model):
    __tablename__ = 'destination'
    
    destinationID = db.Column(db.Integer, primary_key=True)
    adminID = db.Column(db.Integer, db.ForeignKey('admin.adminID'), nullable=True)
    name = db.Column(db.String(50), nullable=False)
    street = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(30), nullable=False)
    description = db.Column(db.Text, nullable=True)
    category = db.Column(db.String(100), nullable=True)
    imageURL = db.Column(db.String(500), nullable=True)  # Added image column
    
    # Relationships
    restaurants = db.relationship('Restaurant', backref='destination', lazy=True)
    transportation = db.relationship('Transportation', backref='destination', lazy=True)
    reviews = db.relationship('Review', backref='destination', lazy=True)
    favourites = db.relationship('Favourite', backref='destination', lazy=True)
    visits = db.relationship('Visit', backref='destination', lazy=True)

class Hotel(db.Model):
    __tablename__ = 'hotel'
    
    hotelID = db.Column(db.Integer, primary_key=True)
    adminID = db.Column(db.Integer, db.ForeignKey('admin.adminID'), nullable=True)
    name = db.Column(db.String(50), nullable=False)
    street = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(30), nullable=False)
    facilities = db.Column(db.Text, nullable=True)
    imageURL = db.Column(db.String(500), nullable=True)  # Added image column
    
    # Relationships
    bookings = db.relationship('Booking', backref='hotel', lazy=True)
    reviews = db.relationship('Review', backref='hotel', lazy=True)

class Restaurant(db.Model):
    __tablename__ = 'restaurant'
    
    restaurantID = db.Column(db.Integer, primary_key=True)
    adminID = db.Column(db.Integer, db.ForeignKey('admin.adminID'), nullable=True)
    destinationID = db.Column(db.Integer, db.ForeignKey('destination.destinationID'), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    street = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(30), nullable=False)
    cuisine = db.Column(db.String(30), nullable=True)
    imageURL = db.Column(db.String(500), nullable=True)  # Added image column
    
    # Relationships
    reservations = db.relationship('Reservation', backref='restaurant', lazy=True)
    reviews = db.relationship('Review', backref='restaurant', lazy=True)

class Booking(db.Model):
    __tablename__ = 'booking'
    
    bookingID = db.Column(db.Integer, primary_key=True)
    userID = db.Column(db.Integer, db.ForeignKey('user.userID'), nullable=False)
    hotelID = db.Column(db.Integer, db.ForeignKey('hotel.hotelID'), nullable=False)
    checkInDate = db.Column(db.Date, nullable=False)
    checkOutDate = db.Column(db.Date, nullable=False)
    roomType = db.Column(db.String(30), nullable=True)
    cost = db.Column(db.Numeric(8, 2), nullable=True)
    bookingDate = db.Column(db.DateTime, default=datetime.utcnow)

class Reservation(db.Model):
    __tablename__ = 'reservation'
    
    reservationID = db.Column(db.Integer, primary_key=True)
    userID = db.Column(db.Integer, db.ForeignKey('user.userID'), nullable=False)
    restaurantID = db.Column(db.Integer, db.ForeignKey('restaurant.restaurantID'), nullable=False)
    reservationDate = db.Column(db.Date, nullable=False)
    reservationTime = db.Column(db.Time, nullable=False)
    numberOfGuests = db.Column(db.Integer, default=1)
    tableNumber = db.Column(db.String(20), nullable=True)

class Transportation(db.Model):
    __tablename__ = 'transportation'
    
    transportationID = db.Column(db.Integer, primary_key=True)
    destinationID = db.Column(db.Integer, db.ForeignKey('destination.destinationID'), nullable=False)
    adminID = db.Column(db.Integer, db.ForeignKey('admin.adminID'), nullable=False)
    type = db.Column(db.String(30), nullable=True)
    provider = db.Column(db.String(50), nullable=True)
    
    # Relationships
    travels = db.relationship('Travel', backref='transportation', lazy=True)
    reviews = db.relationship('Review', backref='transportation', lazy=True)

class Travel(db.Model):
    __tablename__ = 'travel'
    
    travelID = db.Column(db.Integer, primary_key=True)
    userID = db.Column(db.Integer, db.ForeignKey('user.userID'), nullable=False)
    transportationID = db.Column(db.Integer, db.ForeignKey('transportation.transportationID'), nullable=False)
    travelDate = db.Column(db.Date, nullable=False)
    departureTime = db.Column(db.Time, nullable=False)
    arrivalTime = db.Column(db.Time, nullable=False)
    fare = db.Column(db.Numeric(8, 2), nullable=False)
    departurePoint = db.Column(db.String(50), nullable=False)
    arrivalPoint = db.Column(db.String(50), nullable=False)

class Review(db.Model):
    __tablename__ = 'review'
    
    reviewID = db.Column(db.Integer, primary_key=True)
    userID = db.Column(db.Integer, db.ForeignKey('user.userID'), nullable=False)
    destinationID = db.Column(db.Integer, db.ForeignKey('destination.destinationID'), nullable=True)
    restaurantID = db.Column(db.Integer, db.ForeignKey('restaurant.restaurantID'), nullable=True)
    transportationID = db.Column(db.Integer, db.ForeignKey('transportation.transportationID'), nullable=True)
    hotelID = db.Column(db.Integer, db.ForeignKey('hotel.hotelID'), nullable=True)
    rating = db.Column(db.Integer, nullable=False)  # 1-5 rating
    comment = db.Column(db.Text, nullable=True)
    reviewType = db.Column(db.String(50), nullable=True)
    reviewDate = db.Column(db.DateTime, default=datetime.utcnow)

class Favourite(db.Model):
    __tablename__ = 'favourite'
    
    favouriteID = db.Column(db.Integer, primary_key=True)
    userID = db.Column(db.Integer, db.ForeignKey('user.userID'), nullable=False)
    destinationID = db.Column(db.Integer, db.ForeignKey('destination.destinationID'), nullable=False)
    dateAdded = db.Column(db.DateTime, default=datetime.utcnow)

class Visit(db.Model):
    __tablename__ = 'visit'
    
    visitID = db.Column(db.Integer, primary_key=True)
    userID = db.Column(db.Integer, db.ForeignKey('user.userID'), nullable=False)
    destinationID = db.Column(db.Integer, db.ForeignKey('destination.destinationID'), nullable=False)
    visitDate = db.Column(db.Date, nullable=False)
    rating = db.Column(db.Integer, nullable=True)  # 1-5 rating
    notes = db.Column(db.Text, nullable=True)