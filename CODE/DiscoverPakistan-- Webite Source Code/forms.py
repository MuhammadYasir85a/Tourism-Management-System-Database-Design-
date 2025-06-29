from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, DateField, TimeField, IntegerField, DecimalField, PasswordField, EmailField, TelField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, Length, NumberRange, Optional, EqualTo, Regexp

class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])

class RegisterForm(FlaskForm):
    name = StringField('Full Name', validators=[DataRequired(), Length(min=2, max=50)])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', 
                                   validators=[DataRequired(), EqualTo('password')])
    contact_number = TelField('Contact Number', validators=[Optional(), Length(max=15)])

class DestinationForm(FlaskForm):
    name = StringField('Destination Name', validators=[DataRequired(), Length(max=50)])
    street = StringField('Street Address', validators=[DataRequired(), Length(max=100)])
    city = StringField('City', validators=[DataRequired(), Length(max=30)])
    description = TextAreaField('Description', validators=[Optional()])
    category = SelectField('Category', choices=[
        ('Religious Site', 'Religious Site'),
        ('Historical', 'Historical'),
        ('Archaeological', 'Archaeological'),
        ('Natural Landscape', 'Natural Landscape'),
        ('Adventure', 'Adventure'),
        ('Monument', 'Monument'),
        ('Museum', 'Museum'),
        ('Historical Garden', 'Historical Garden')
    ], validators=[Optional()])
    imageURL = StringField('Image URL', validators=[Optional(), Length(max=500)])

class HotelForm(FlaskForm):
    name = StringField('Hotel Name', validators=[DataRequired(), Length(max=50)])
    street = StringField('Street Address', validators=[DataRequired(), Length(max=100)])
    city = StringField('City', validators=[DataRequired(), Length(max=30)])
    facilities = TextAreaField('Facilities', validators=[Optional()])
    imageURL = StringField('Image URL', validators=[Optional(), Length(max=500)])

class RestaurantForm(FlaskForm):
    name = StringField('Restaurant Name', validators=[DataRequired(), Length(max=50)])
    street = StringField('Street Address', validators=[DataRequired(), Length(max=100)])
    city = StringField('City', validators=[DataRequired(), Length(max=30)])
    cuisine = StringField('Cuisine Type', validators=[Optional(), Length(max=30)])
    destinationID = SelectField('Associated Destination', coerce=int, validators=[DataRequired()])
    imageURL = StringField('Image URL', validators=[Optional(), Length(max=500)])

class BookingForm(FlaskForm):
    checkInDate = DateField('Check-in Date', validators=[DataRequired()])
    checkOutDate = DateField('Check-out Date', validators=[DataRequired()])
    roomType = SelectField('Room Type', choices=[
        ('Standard', 'Standard'),
        ('Deluxe', 'Deluxe'),
        ('Executive', 'Executive'),
        ('Suite', 'Suite'),
        ('Mountain View', 'Mountain View'),
        ('Sea View', 'Sea View'),
        ('Lake View', 'Lake View')
    ], validators=[Optional()])

class ReservationForm(FlaskForm):
    reservationDate = DateField('Reservation Date', validators=[DataRequired()])
    reservationTime = TimeField('Reservation Time', validators=[DataRequired()])
    numberOfGuests = IntegerField('Number of Guests', 
                                validators=[DataRequired(), NumberRange(min=1, max=20)])

class ReviewForm(FlaskForm):
    rating = SelectField('Rating', choices=[
        (5, '5 Stars - Excellent'),
        (4, '4 Stars - Very Good'),
        (3, '3 Stars - Good'),
        (2, '2 Stars - Fair'),
        (1, '1 Star - Poor')
    ], coerce=int, validators=[DataRequired()])
    comment = TextAreaField('Comment', validators=[Optional(), Length(max=1000)])

class EditProfileForm(FlaskForm):
    name = StringField('Full Name', validators=[
        DataRequired(message='Please enter your full name'),
        Length(min=2, max=50, message='Name must be between 2 and 50 characters')
    ])
    email = EmailField('Email', validators=[
        DataRequired(message='Please enter your email'),
        Email(message='Please enter a valid email address'),
        Length(max=100, message='Email must be less than 100 characters')
    ])
    contact_number = StringField('Contact Number', validators=[
        Optional(),
        Length(max=15, message='Contact number must be less than 15 characters'),
        Regexp(r'^\+?[\d\s-]+$', message='Please enter a valid phone number')
    ])
    submit = SubmitField('Save Changes')

class DeleteAccountForm(FlaskForm):
    confirm_delete = BooleanField('I understand that this action is permanent and cannot be undone', 
                                validators=[DataRequired(message='You must confirm that you understand this action is permanent')])
    submit = SubmitField('Delete Account')
