import os
import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from werkzeug.middleware.proxy_fix import ProxyFix
from flask_wtf.csrf import CSRFProtect

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Initialize these variables at module level but don't bind to app yet
db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()
csrf = CSRFProtect()

def create_app():
    app = Flask(__name__)
    
    # Configuration
    app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key-change-in-production")
    app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)
    
    # Initialize CSRF protection
    csrf.init_app(app)
    
    # Database configuration for MySQL
    database_url = os.environ.get("DATABASE_URL", "mysql+pymysql://root:password@localhost/TourismManagementSystem")
    app.config["SQLALCHEMY_DATABASE_URI"] = database_url
    app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
        "pool_recycle": 300,
        "pool_pre_ping": True,
    }
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    
    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    
    # Login manager configuration
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'info'
    
    @login_manager.user_loader
    def load_user(user_id):
        from models import User, Admin
        # Try to load as Admin first
        admin = Admin.query.get(int(user_id))
        if admin:
            return admin
        return User.query.get(int(user_id)) 
    # Import routes and register blueprints
    with app.app_context():
        import routes
        app.register_blueprint(routes.main_bp)
        app.register_blueprint(routes.auth_bp, url_prefix='/auth')
        app.register_blueprint(routes.destinations_bp, url_prefix='/destinations')
        app.register_blueprint(routes.hotels_bp, url_prefix='/hotels')
        app.register_blueprint(routes.restaurants_bp, url_prefix='/restaurants')
        app.register_blueprint(routes.user_bp, url_prefix='/user')
        app.register_blueprint(routes.admin_bp, url_prefix='/admin')
    
    # Initialize models and create tables
    with app.app_context():
        db.create_all()
    
    return app

# Create the app instance
app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
