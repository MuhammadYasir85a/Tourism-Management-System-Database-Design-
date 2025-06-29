from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, abort
from flask_login import login_user, logout_user, login_required, current_user
from datetime import datetime, date
from werkzeug.security import generate_password_hash
# Import db in a way that avoids circular imports
import app
db = app.db
from models import *
from forms import *
from functools import wraps
import logging

# Create blueprints
main_bp = Blueprint('main', __name__)
auth_bp = Blueprint('auth', __name__)
destinations_bp = Blueprint('destinations', __name__)
hotels_bp = Blueprint('hotels', __name__)
restaurants_bp = Blueprint('restaurants', __name__)
user_bp = Blueprint('user', __name__)
admin_bp = Blueprint('admin', __name__)



# Main routes
@main_bp.route('/')
def index():
    # Get featured destinations, hotels, and restaurants
    destinations = Destination.query.limit(6).all()
    hotels = Hotel.query.limit(4).all()
    restaurants = Restaurant.query.limit(3).all()
    
    return render_template('index.html', 
                         destinations=destinations, 
                         hotels=hotels, 
                         restaurants=restaurants)

@main_bp.route('/terms-of-service')
def terms_of_service():
    return render_template('legal/terms_of_service.html')

@main_bp.route('/privacy-policy')
def privacy_policy():
    return render_template('legal/privacy_policy.html')

@main_bp.route('/about')
def about():
    return render_template('about.html')

@main_bp.route('/contact')
def contact():
    return render_template('contact.html')

# Authentication routes
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        # First, check if the user is an admin
        admin = Admin.query.filter_by(email=form.email.data).first()
        if admin and admin.check_password(form.password.data):
            login_user(admin)
            flash('Admin login successful!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('admin.dashboard'))
        # If not admin, check regular user
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash('Login successful!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.index'))
        else:
            flash('Invalid email or password', 'danger')
    
    return render_template('auth/login.html', form=form)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = RegisterForm()
    if form.validate_on_submit():
        # Check if user already exists
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user:
            flash('Email already registered', 'danger')
            return render_template('auth/register.html', form=form)
        
        # Create new user
        new_user_id = User.query.count() + 101  # Start from 101 like in sample data
        user = User(
            userID=new_user_id,
            name=form.name.data,
            email=form.email.data,
            contactNumber=form.contact_number.data
        )
        user.set_password(form.password.data)
        
        db.session.add(user)
        db.session.commit()
        
        login_user(user)
        flash('Registration successful!', 'success')
        return redirect(url_for('main.index'))
    
    return render_template('auth/register.html', form=form)

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out', 'info')
    return redirect(url_for('main.index'))

# Destination routes
@destinations_bp.route('/')
def index():
    search = request.args.get('search', '')
    category = request.args.get('category', '')
    
    query = Destination.query
    
    if search:
        query = query.filter(Destination.name.contains(search) | 
                           Destination.city.contains(search) |
                           Destination.description.contains(search))
    
    if category:
        query = query.filter(Destination.category == category)
    
    destinations = query.all()
    categories = db.session.query(Destination.category).distinct().all()
    categories = [cat[0] for cat in categories if cat[0]]
    
    return render_template('destinations/index.html', 
                         destinations=destinations, 
                         categories=categories,
                         search=search,
                         selected_category=category)

@destinations_bp.route('/<int:destination_id>')
def detail(destination_id):
    destination = Destination.query.get_or_404(destination_id)
    restaurants = Restaurant.query.filter_by(destinationID=destination_id).all()
    reviews = Review.query.filter_by(destinationID=destination_id).all()
    
    # Check if user has favorited this destination
    is_favorited = False
    if current_user.is_authenticated:
        is_favorited = Favourite.query.filter_by(
            destinationID=destination_id, 
            userID=current_user.userID
        ).first() is not None
    
    return render_template('destinations/detail.html', 
                         destination=destination,
                         restaurants=restaurants,
                         reviews=reviews,
                         is_favorited=is_favorited)

@destinations_bp.route('/<int:destination_id>/favorite', methods=['POST'])
@login_required
def toggle_favorite(destination_id):
    destination = Destination.query.get_or_404(destination_id)
    favorite = Favourite.query.filter_by(
        destinationID=destination_id,
        userID=current_user.userID
    ).first()
    if favorite:
        db.session.delete(favorite)
        db.session.commit()
        if request.is_json:
            return jsonify(success=True, action="removed")
        flash('Removed from favorites', 'info')
    else:
        favorite = Favourite(
            destinationID=destination_id,
            userID=current_user.userID,
            dateAdded=datetime.utcnow()
        )
        db.session.add(favorite)
        db.session.commit()
        if request.is_json:
            return jsonify(success=True, action="added")
        flash('Added to favorites', 'success')
    if request.is_json:
        return jsonify(success=False)
    return redirect(url_for('destinations.detail', destination_id=destination_id))

# Hotel routes
@hotels_bp.route('/')
def index():
    search = request.args.get('search', '')
    city = request.args.get('city', '')
    
    query = Hotel.query
    
    if search:
        query = query.filter(Hotel.name.contains(search) | 
                           Hotel.facilities.contains(search))
    
    if city:
        query = query.filter(Hotel.city == city)
    
    hotels = query.all()
    cities = db.session.query(Hotel.city).distinct().all()
    cities = [city[0] for city in cities if city[0]]
    
    return render_template('hotels/index.html', 
                         hotels=hotels, 
                         cities=cities,
                         search=search,
                         selected_city=city)

@hotels_bp.route('/<int:hotel_id>')
def detail(hotel_id):
    hotel = Hotel.query.get_or_404(hotel_id)
    reviews = Review.query.filter_by(hotelID=hotel_id).all()
    
    return render_template('hotels/detail.html', hotel=hotel, reviews=reviews)

@hotels_bp.route('/<int:hotel_id>/book', methods=['GET', 'POST'])
@login_required
def book(hotel_id):
    hotel = Hotel.query.get_or_404(hotel_id)
    form = BookingForm()
    
    if form.validate_on_submit():
        # Generate new booking ID
        new_booking_id = Booking.query.count() + 401  # Start from 401 like in sample data
        
        booking = Booking(
            bookingID=new_booking_id,
            userID=current_user.userID,
            hotelID=hotel_id,
            checkInDate=form.checkInDate.data,
            checkOutDate=form.checkOutDate.data,
            roomType=form.roomType.data,
            bookingDate=datetime.utcnow()
        )
        
        db.session.add(booking)
        db.session.commit()
        
        flash('Booking confirmed!', 'success')
        return redirect(url_for('user.bookings'))
    
    return render_template('hotels/booking.html', hotel=hotel, form=form)

# Restaurant routes
@restaurants_bp.route('/')
def index():
    search = request.args.get('search', '')
    cuisine = request.args.get('cuisine', '')
    
    query = Restaurant.query
    
    if search:
        query = query.filter(Restaurant.name.contains(search) | 
                           Restaurant.city.contains(search))
    
    if cuisine:
        query = query.filter(Restaurant.cuisine == cuisine)
    
    restaurants = query.all()
    cuisines = db.session.query(Restaurant.cuisine).distinct().all()
    cuisines = [cuisine[0] for cuisine in cuisines if cuisine[0]]
    
    return render_template('restaurants/index.html', 
                         restaurants=restaurants, 
                         cuisines=cuisines,
                         search=search,
                         selected_cuisine=cuisine)

@restaurants_bp.route('/<int:restaurant_id>')
def detail(restaurant_id):
    restaurant = Restaurant.query.get_or_404(restaurant_id)
    reviews = Review.query.filter_by(restaurantID=restaurant_id).all()
    
    return render_template('restaurants/detail.html', restaurant=restaurant, reviews=reviews)

@restaurants_bp.route('/<int:restaurant_id>/reserve', methods=['GET', 'POST'])
@login_required
def reserve(restaurant_id):
    restaurant = Restaurant.query.get_or_404(restaurant_id)
    form = ReservationForm()
    
    if form.validate_on_submit():
        # Generate new reservation ID
        new_reservation_id = Reservation.query.count() + 601  # Start from 601 like in sample data
        
        reservation = Reservation(
            reservationID=new_reservation_id,
            userID=current_user.userID,
            restaurantID=restaurant_id,
            reservationDate=form.reservationDate.data,
            reservationTime=form.reservationTime.data,
            numberOfGuests=form.numberOfGuests.data
        )
        
        db.session.add(reservation)
        db.session.commit()
        
        flash('Reservation confirmed!', 'success')
        return redirect(url_for('user.dashboard'))
    
    return render_template('restaurants/reservation.html', restaurant=restaurant, form=form)

# User routes
@user_bp.route('/dashboard')
@login_required
def dashboard():
    recent_bookings = Booking.query.filter_by(userID=current_user.userID).order_by(Booking.bookingDate.desc()).limit(5).all()
    recent_reservations = Reservation.query.filter_by(userID=current_user.userID).limit(5).all()
    favorite_count = Favourite.query.filter_by(userID=current_user.userID).count()
    
    # Create delete account form
    form = DeleteAccountForm()
    
    return render_template('user/dashboard.html', 
                         recent_bookings=recent_bookings,
                         recent_reservations=recent_reservations,
                         favorite_count=favorite_count,
                         form=form)

@user_bp.route('/bookings')
@login_required
def bookings():
    bookings = Booking.query.filter_by(userID=current_user.userID).order_by(Booking.bookingDate.desc()).all()
    return render_template('user/bookings.html', bookings=bookings)

@user_bp.route('/favorites')
@login_required
def favorites():
    favorites = db.session.query(Favourite, Destination).join(Destination).filter(Favourite.userID == current_user.userID).all()
    return render_template('user/favorites.html', favorites=favorites)

@user_bp.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if request.method == 'GET':
        # Pre-populate form with current user data
        form.name.data = current_user.name
        form.email.data = current_user.email
        form.contact_number.data = current_user.contactNumber
    
    if form.validate_on_submit():
        # Check if email is taken by another user
        if form.email.data != current_user.email:
            existing_user = User.query.filter_by(email=form.email.data).first()
            if existing_user:
                flash('Email already in use by another account.', 'danger')
                return render_template('user/edit_profile.html', form=form)
        
        # Update user data
        current_user.name = form.name.data
        current_user.email = form.email.data
        current_user.contactNumber = form.contact_number.data
        db.session.commit()
        
        flash('Your profile has been updated successfully.', 'success')
        return redirect(url_for('user.dashboard'))
    
    return render_template('user/edit_profile.html', form=form)

@user_bp.route('/delete-account', methods=['POST'])
@login_required
def delete_account():
    try:
        # Verify the confirmation checkbox was checked
        if not request.form.get('confirm_delete'):
            flash('Please confirm that you understand the consequences of account deletion.', 'danger')
            return redirect(url_for('user.dashboard'))

        user = User.query.get(current_user.userID)
        if not user:
            flash('User account not found.', 'danger')
            return redirect(url_for('user.dashboard'))

        # Delete related records in order
        Review.query.filter_by(userID=user.userID).delete()
        Visit.query.filter_by(userID=user.userID).delete()
        Favourite.query.filter_by(userID=user.userID).delete()
        Reservation.query.filter_by(userID=user.userID).delete()
        Booking.query.filter_by(userID=user.userID).delete()

        # Delete the user
        db.session.delete(user)
        db.session.commit()

        # Log out the user and redirect to home
        logout_user()
        flash('Your account has been successfully deleted.', 'success')
        return redirect(url_for('main.index'))

        # Log out the user
        logout_user()
        
        return jsonify({
            'success': True, 
            'message': 'Account deleted successfully',
            'redirect': url_for('main.index')
        })

    except Exception as e:
        db.session.rollback()
        logging.error(f"Delete account error: {str(e)}")
        return jsonify({
            'success': False, 
            'message': 'Account deletion failed. Please contact support.'
        }), 500

# Admin routes
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not hasattr(current_user, 'adminID'):
            abort(403)  # Forbidden
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('/dashboard')
@login_required
@admin_required
def dashboard():
    total_destinations = Destination.query.count()
    total_hotels = Hotel.query.count()
    total_restaurants = Restaurant.query.count()
    total_bookings = Booking.query.count()
    
    return render_template('admin/dashboard.html',
                         total_destinations=total_destinations,
                         total_hotels=total_hotels,
                         total_restaurants=total_restaurants,
                         total_bookings=total_bookings)

@admin_bp.route('/destinations')
@login_required
@admin_required
def destinations():
    destinations = Destination.query.all()
    return render_template('admin/destinations.html', destinations=destinations)

@admin_bp.route('/destinations/<int:destination_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_destination(destination_id):
    try:
        destination = Destination.query.get_or_404(destination_id)
        
        # Delete associated records first
        # Restaurants at this destination
        restaurants = Restaurant.query.filter_by(destinationID=destination_id).all()
        for restaurant in restaurants:
            # Delete reservations for this restaurant
            Reservation.query.filter_by(restaurantID=restaurant.restaurantID).delete()
            # Delete reviews for this restaurant
            Review.query.filter_by(restaurantID=restaurant.restaurantID).delete()
            # Delete the restaurant
            db.session.delete(restaurant)
        
        # Delete favorites for this destination
        Favourite.query.filter_by(destinationID=destination_id).delete()
        
        # Delete visits for this destination
        Visit.query.filter_by(destinationID=destination_id).delete()
        
        # Delete reviews for this destination
        Review.query.filter_by(destinationID=destination_id).delete()
        
        # Delete transportation for this destination
        transportations = Transportation.query.filter_by(destinationID=destination_id).all()
        for transportation in transportations:
            # Delete travels for this transportation
            Travel.query.filter_by(transportationID=transportation.transportationID).delete()
            # Delete the transportation
            db.session.delete(transportation)
        
        # Finally delete the destination
        db.session.delete(destination)
        db.session.commit()
        
        return jsonify({'success': True, 'message': f'Destination {destination.name} deleted successfully'})
    except Exception as e:
        db.session.rollback()
        logging.error(f"Error deleting destination: {str(e)}")
        return jsonify({'success': False, 'message': f'Error deleting destination: {str(e)}'}), 500

@admin_bp.route('/hotels')
@login_required
@admin_required
def hotels():
    hotels = Hotel.query.all()
    return render_template('admin/hotels.html', hotels=hotels)

@admin_bp.route('/hotels/<int:hotel_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_hotel(hotel_id):
    try:
        hotel = Hotel.query.get_or_404(hotel_id)
        
        # Delete bookings for this hotel
        Booking.query.filter_by(hotelID=hotel_id).delete()
        
        # Delete reviews for this hotel
        Review.query.filter_by(hotelID=hotel_id).delete()
        
        # Delete the hotel
        db.session.delete(hotel)
        db.session.commit()
        
        return jsonify({'success': True, 'message': f'Hotel {hotel.name} deleted successfully'})
    except Exception as e:
        db.session.rollback()
        logging.error(f"Error deleting hotel: {str(e)}")
        return jsonify({'success': False, 'message': f'Error deleting hotel: {str(e)}'}), 500

@admin_bp.route('/restaurants')
@login_required
@admin_required
def restaurants():
    restaurants = Restaurant.query.all()
    return render_template('admin/restaurants.html', restaurants=restaurants)

@admin_bp.route('/restaurants/<int:restaurant_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_restaurant(restaurant_id):
    try:
        restaurant = Restaurant.query.get_or_404(restaurant_id)
        
        # Delete reservations for this restaurant
        Reservation.query.filter_by(restaurantID=restaurant_id).delete()
        
        # Delete reviews for this restaurant
        Review.query.filter_by(restaurantID=restaurant_id).delete()
        
        # Delete the restaurant
        db.session.delete(restaurant)
        db.session.commit()
        
        return jsonify({'success': True, 'message': f'Restaurant {restaurant.name} deleted successfully'})
    except Exception as e:
        db.session.rollback()
        logging.error(f"Error deleting restaurant: {str(e)}")
        return jsonify({'success': False, 'message': f'Error deleting restaurant: {str(e)}'}), 500
