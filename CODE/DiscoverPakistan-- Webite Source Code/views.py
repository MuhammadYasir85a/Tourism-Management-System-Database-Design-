from flask import render_template, request, redirect, url_for, flash, session, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import func, and_, or_
from datetime import datetime, date
from app import app, db
from models import *
from forms import *
from utils import admin_required

@app.route('/')
def index():
    """Homepage with featured destinations"""
    featured_destinations = Destination.query.limit(6).all()
    return render_template('index.html', destinations=featured_destinations)

@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash('Welcome back!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        flash('Invalid email or password', 'danger')
    
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration"""
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        # Generate next user ID
        max_user_id = db.session.query(func.max(User.userID)).scalar() or 100
        
        user = User(
            userID=max_user_id + 1,
            name=form.name.data,
            email=form.email.data,
            contactNumber=form.contact_number.data
        )
        user.set_password(form.password.data)
        
        db.session.add(user)
        db.session.commit()
        
        flash('Registration successful! You can now log in.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html', form=form)

@app.route('/logout')
@login_required
def logout():
    """User logout"""
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

@app.route('/destinations')
def destinations():
    """Browse all destinations with search and filter"""
    search = request.args.get('search', '')
    category = request.args.get('category', '')
    city = request.args.get('city', '')
    
    query = Destination.query
    
    if search:
        query = query.filter(or_(
            Destination.name.contains(search),
            Destination.description.contains(search)
        ))
    
    if category:
        query = query.filter(Destination.category == category)
    
    if city:
        query = query.filter(Destination.city == city)
    
    destinations = query.all()
    
    # Get unique categories and cities for filters
    categories = db.session.query(Destination.category).distinct().all()
    cities = db.session.query(Destination.city).distinct().all()
    
    return render_template('destinations.html', 
                         destinations=destinations,
                         categories=[c[0] for c in categories if c[0]],
                         cities=[c[0] for c in cities if c[0]],
                         search=search,
                         selected_category=category,
                         selected_city=city)

@app.route('/destination/<int:destination_id>')
def destination_detail(destination_id):
    """Destination detail page"""
    destination = Destination.query.get_or_404(destination_id)
    
    # Get restaurants at this destination
    restaurants = Restaurant.query.filter_by(destinationID=destination_id).all()
    
    # Get reviews for this destination
    reviews = Review.query.filter_by(destinationID=destination_id).all()
    
    # Check if user has favorited this destination
    is_favorite = False
    if current_user.is_authenticated:
        is_favorite = Favourite.query.filter_by(
            destinationID=destination_id, 
            userID=current_user.userID
        ).first() is not None
    
    return render_template('destination_detail.html', 
                         destination=destination,
                         restaurants=restaurants,
                         reviews=reviews,
                         is_favorite=is_favorite)

@app.route('/favorite/<int:destination_id>', methods=['POST'])
@login_required
def toggle_favorite(destination_id):
    """Toggle destination favorite status"""
    destination = Destination.query.get_or_404(destination_id)
    
    favorite = Favourite.query.filter_by(
        destinationID=destination_id,
        userID=current_user.userID
    ).first()
    
    if favorite:
        db.session.delete(favorite)
        flash('Removed from favorites', 'info')
    else:
        favorite = Favourite(
            destinationID=destination_id,
            userID=current_user.userID,
            favouriteDate=date.today()
        )
        db.session.add(favorite)
        flash('Added to favorites', 'success')
    
    db.session.commit()
    return redirect(url_for('destination_detail', destination_id=destination_id))

@app.route('/mark_visited/<int:destination_id>', methods=['POST'])
@login_required
def mark_visited(destination_id):
    """Mark destination as visited"""
    destination = Destination.query.get_or_404(destination_id)
    
    visit = Visit.query.filter_by(
        destinationID=destination_id,
        userID=current_user.userID
    ).first()
    
    if not visit:
        visit = Visit(
            destinationID=destination_id,
            userID=current_user.userID,
            visitDate=date.today()
        )
        db.session.add(visit)
        db.session.commit()
        flash('Marked as visited!', 'success')
    else:
        flash('Already marked as visited', 'info')
    
    return redirect(url_for('destination_detail', destination_id=destination_id))

@app.route('/hotels')
def hotels():
    """Browse all hotels"""
    search = request.args.get('search', '')
    city = request.args.get('city', '')
    
    query = Hotel.query
    
    if search:
        query = query.filter(or_(
            Hotel.name.contains(search),
            Hotel.facilities.contains(search)
        ))
    
    if city:
        query = query.filter(Hotel.city == city)
    
    hotels = query.all()
    
    # Get unique cities for filters
    cities = db.session.query(Hotel.city).distinct().all()
    
    return render_template('hotels.html', 
                         hotels=hotels,
                         cities=[c[0] for c in cities if c[0]],
                         search=search,
                         selected_city=city)

@app.route('/hotel/<int:hotel_id>')
def hotel_detail(hotel_id):
    """Hotel detail page"""
    hotel = Hotel.query.get_or_404(hotel_id)
    
    # Get reviews for this hotel
    reviews = Review.query.filter_by(hotelID=hotel_id).all()
    
    return render_template('hotel_detail.html', hotel=hotel, reviews=reviews)

@app.route('/book_hotel/<int:hotel_id>', methods=['GET', 'POST'])
@login_required
def book_hotel(hotel_id):
    """Book a hotel room"""
    hotel = Hotel.query.get_or_404(hotel_id)
    form = BookingForm()
    
    if form.validate_on_submit():
        if form.check_out_date.data <= form.check_in_date.data:
            flash('Check-out date must be after check-in date', 'danger')
            return render_template('book_hotel.html', hotel=hotel, form=form)
        
        # Calculate cost (simple pricing logic)
        days = (form.check_out_date.data - form.check_in_date.data).days
        base_cost = {'Standard': 80, 'Deluxe': 120, 'Executive': 150, 'Suite': 200, 
                    'Business': 140, 'Mountain View': 130, 'Sea View': 140, 
                    'Lake View': 110, 'Valley View': 150}.get(form.room_type.data, 100)
        total_cost = base_cost * days
        
        # Generate next booking ID
        max_booking_id = db.session.query(func.max(Booking.bookingID)).scalar() or 400
        
        booking = Booking(
            bookingID=max_booking_id + 1,
            userID=current_user.userID,
            hotelID=hotel_id,
            checkInDate=form.check_in_date.data,
            checkOutDate=form.check_out_date.data,
            roomType=form.room_type.data,
            cost=total_cost
        )
        
        db.session.add(booking)
        db.session.commit()
        
        flash(f'Hotel booked successfully! Total cost: ${total_cost}', 'success')
        return redirect(url_for('profile'))
    
    return render_template('book_hotel.html', hotel=hotel, form=form)

@app.route('/restaurants')
def restaurants():
    """Browse all restaurants"""
    search = request.args.get('search', '')
    city = request.args.get('city', '')
    cuisine = request.args.get('cuisine', '')
    
    query = Restaurant.query
    
    if search:
        query = query.filter(or_(
            Restaurant.name.contains(search),
            Restaurant.cuisine.contains(search)
        ))
    
    if city:
        query = query.filter(Restaurant.city == city)
    
    if cuisine:
        query = query.filter(Restaurant.cuisine == cuisine)
    
    restaurants = query.all()
    
    # Get unique cities and cuisines for filters
    cities = db.session.query(Restaurant.city).distinct().all()
    cuisines = db.session.query(Restaurant.cuisine).distinct().all()
    
    return render_template('restaurants.html', 
                         restaurants=restaurants,
                         cities=[c[0] for c in cities if c[0]],
                         cuisines=[c[0] for c in cuisines if c[0]],
                         search=search,
                         selected_city=city,
                         selected_cuisine=cuisine)

@app.route('/restaurant/<int:restaurant_id>')
def restaurant_detail(restaurant_id):
    """Restaurant detail page"""
    restaurant = Restaurant.query.get_or_404(restaurant_id)
    
    # Get reviews for this restaurant
    reviews = Review.query.filter_by(restaurantID=restaurant_id).all()
    
    return render_template('restaurant_detail.html', restaurant=restaurant, reviews=reviews)

@app.route('/make_reservation/<int:restaurant_id>', methods=['GET', 'POST'])
@login_required
def make_reservation(restaurant_id):
    """Make a restaurant reservation"""
    restaurant = Restaurant.query.get_or_404(restaurant_id)
    form = ReservationForm()
    
    if form.validate_on_submit():
        if form.reservation_date.data < date.today():
            flash('Reservation date cannot be in the past', 'danger')
            return render_template('make_reservation.html', restaurant=restaurant, form=form)
        
        # Generate next reservation ID
        max_reservation_id = db.session.query(func.max(Reservation.reservationID)).scalar() or 600
        
        reservation = Reservation(
            reservationID=max_reservation_id + 1,
            userID=current_user.userID,
            restaurantID=restaurant_id,
            reservationDate=form.reservation_date.data,
            reservationTime=form.reservation_time.data,
            numberOfGuests=form.number_of_guests.data
        )
        
        db.session.add(reservation)
        db.session.commit()
        
        flash('Reservation made successfully!', 'success')
        return redirect(url_for('profile'))
    
    return render_template('make_reservation.html', restaurant=restaurant, form=form)

@app.route('/profile')
@login_required
def profile():
    """User profile page"""
    # Get user's bookings
    bookings = Booking.query.filter_by(userID=current_user.userID).all()
    
    # Get user's reservations
    reservations = Reservation.query.filter_by(userID=current_user.userID).all()
    
    # Get user's favorites
    favorites = db.session.query(Favourite, Destination).join(
        Destination, Favourite.destinationID == Destination.destinationID
    ).filter(Favourite.userID == current_user.userID).all()
    
    # Get user's visits
    visits = db.session.query(Visit, Destination).join(
        Destination, Visit.destinationID == Destination.destinationID
    ).filter(Visit.userID == current_user.userID).all()
    
    return render_template('profile.html', 
                         bookings=bookings, 
                         reservations=reservations,
                         favorites=favorites,
                         visits=visits)

@app.route('/submit_review/<review_type>/<int:item_id>', methods=['GET', 'POST'])
@login_required
def submit_review(review_type, item_id):
    """Submit a review for destination, hotel, restaurant, or transportation"""
    form = ReviewForm()
    
    if form.validate_on_submit():
        # Generate next review ID
        max_review_id = db.session.query(func.max(Review.reviewID)).scalar() or 900
        
        review = Review(
            reviewID=max_review_id + 1,
            userID=current_user.userID,
            rating=form.rating.data,
            comment=form.comment.data,
            reviewType=review_type
        )
        
        # Set the appropriate foreign key based on review type
        if review_type == 'destination':
            review.destinationID = item_id
        elif review_type == 'hotel':
            review.hotelID = item_id
        elif review_type == 'restaurant':
            review.restaurantID = item_id
        elif review_type == 'transportation':
            review.transportationID = item_id
        
        db.session.add(review)
        db.session.commit()
        
        flash('Review submitted successfully!', 'success')
        return redirect(url_for(f'{review_type}_detail', **{f'{review_type}_id': item_id}))
    
    return render_template('submit_review.html', form=form, review_type=review_type)

# Admin routes
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    """Admin login"""
    form = AdminLoginForm()
    if form.validate_on_submit():
        admin = Admin.query.filter_by(email=form.email.data).first()
        if admin and admin.check_password(form.password.data):
            login_user(admin)
            session['is_admin'] = True
            flash('Welcome to Admin Panel!', 'success')
            return redirect(url_for('admin_dashboard'))
        flash('Invalid admin credentials', 'danger')
    
    return render_template('login.html', form=form, is_admin=True)

@app.route('/admin/dashboard')
@login_required
@admin_required
def admin_dashboard():
    """Admin dashboard"""
    stats = {
        'destinations': Destination.query.count(),
        'hotels': Hotel.query.count(),
        'restaurants': Restaurant.query.count(),
        'users': User.query.count(),
        'bookings': Booking.query.count(),
        'reservations': Reservation.query.count()
    }
    
    return render_template('admin/dashboard.html', stats=stats)

@app.route('/admin/destinations')
@login_required
@admin_required
def admin_destinations():
    """Admin manage destinations"""
    destinations = Destination.query.all()
    return render_template('admin/destinations.html', destinations=destinations)

@app.route('/admin/destinations/add', methods=['GET', 'POST'])
@login_required
@admin_required
def admin_add_destination():
    """Admin add destination"""
    form = DestinationForm()
    
    if form.validate_on_submit():
        # Generate next destination ID
        max_dest_id = db.session.query(func.max(Destination.destinationID)).scalar() or 200
        
        destination = Destination(
            destinationID=max_dest_id + 1,
            adminID=current_user.adminID,
            name=form.name.data,
            street=form.street.data,
            city=form.city.data,
            description=form.description.data,
            category=form.category.data,
            imageURL=form.image_url.data
        )
        
        db.session.add(destination)
        db.session.commit()
        
        flash('Destination added successfully!', 'success')
        return redirect(url_for('admin_destinations'))
    
    return render_template('admin/add_destination.html', form=form)

@app.route('/admin/hotels')
@login_required
@admin_required
def admin_hotels():
    """Admin manage hotels"""
    hotels = Hotel.query.all()
    return render_template('admin/hotels.html', hotels=hotels)

@app.route('/admin/restaurants')
@login_required
@admin_required
def admin_restaurants():
    """Admin manage restaurants"""
    restaurants = Restaurant.query.all()
    return render_template('admin/restaurants.html', restaurants=restaurants)
