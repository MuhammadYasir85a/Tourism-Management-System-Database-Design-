from functools import wraps
from flask import session, flash, redirect, url_for
from flask_login import current_user

def admin_required(f):
    """Decorator to require admin authentication"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('Please log in as admin to access this page.', 'warning')
            return redirect(url_for('admin_login'))
        
        if not session.get('is_admin'):
            flash('Admin access required.', 'danger')
            return redirect(url_for('index'))
        
        return f(*args, **kwargs)
    return decorated_function

def calculate_average_rating(reviews):
    """Calculate average rating from reviews"""
    if not reviews:
        return 0
    return sum(review.rating for review in reviews) / len(reviews)

def format_currency(amount):
    """Format currency for display"""
    return f"${amount:.2f}" if amount else "N/A"
