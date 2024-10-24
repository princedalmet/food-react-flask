from flask import Flask, request, jsonify, session
from flask_cors import CORS
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from datetime import timedelta, datetime
from restaurant import app, db, bcrypt
from restaurant.models import User, Item
import logging
import secrets

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize LoginManager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.session_protection = "strong"

# Generate a secure secret key if not already set
if not app.config.get('SECRET_KEY'):
    app.config['SECRET_KEY'] = secrets.token_hex(32)

# Configure Flask app
app.config.update(
    SESSION_COOKIE_SAMESITE='Lax',
    SESSION_COOKIE_SECURE=False,  # Set to True in production with HTTPS
    SESSION_COOKIE_HTTPONLY=True,
    PERMANENT_SESSION_LIFETIME=timedelta(days=1),
    REMEMBER_COOKIE_DURATION=timedelta(days=14),
    REMEMBER_COOKIE_SECURE=False,  # Set to True in production
    REMEMBER_COOKIE_HTTPONLY=True
)

# Configure CORS
CORS(app, 
     resources={r"/*": {
         "origins": ["http://localhost:3000"],
         "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
         "allow_headers": ["Content-Type", "Authorization"],
         "supports_credentials": True
     }})

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@login_manager.unauthorized_handler
def unauthorized():
    return jsonify({"error": "Please log in to access this resource"}), 401

# Registration route
@app.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        logger.info(f"Received registration request for email: {data.get('email')}")

        # Validate required fields
        required_fields = ['first_name', 'last_name', 'email', 'password']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'{field} is required'}), 400

        # Check if user already exists
        if User.query.filter_by(email=data['email']).first():
            return jsonify({'error': 'Email already registered'}), 409

        # Create new user
        new_user = User(
            first_name=data['first_name'],
            last_name=data['last_name'],
            email=data['email'],
            password=data['password'],
            phone_number=data.get('phone_number'),
            role=data.get('role', 'customer')
        )

        db.session.add(new_user)
        db.session.commit()

        logger.info(f"Successfully registered user: {new_user.email}")
        return jsonify({'message': 'Registration successful'}), 201

    except Exception as e:
        logger.exception("Registration error")
        db.session.rollback()
        return jsonify({'error': 'Registration failed. Please try again.'}), 500

@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        remember = data.get('remember', False)

        logger.info(f"Login attempt for email: {email}")

        if not email or not password:
            return jsonify({'error': 'Email and password are required'}), 400

        user = User.query.filter_by(email=email).first()

        if user and user.check_password_correction(password):
            login_user(user, remember=remember)
            session.permanent = True
            user.update_last_login()
            
            logger.info(f"Successful login for user: {email}")
            return jsonify({
                'message': 'Login successful',
                'user': user.to_dict()
            }), 200
        else:
            logger.warning(f"Failed login attempt for email: {email}")
            return jsonify({'error': 'Invalid email or password'}), 401
            
    except Exception as e:
        logger.exception("Login error")
        return jsonify({'error': str(e)}), 500

@app.route('/logout', methods=['POST'])
@login_required
def logout():
    try:
        email = current_user.email
        logout_user()
        session.clear()
        logger.info(f"User logged out: {email}")
        return jsonify({'message': 'Logout successful'}), 200
    except Exception as e:
        logger.exception("Logout error")
        return jsonify({'error': 'Logout failed'}), 500

@app.route('/api/menu', methods=['GET'])
@login_required
def get_menu():
    try:
        items = Item.query.all()
        return jsonify([item.to_dict() for item in items]), 200
    except Exception as e:
        logger.exception("Error retrieving menu items")
        return jsonify({'error': 'Failed to retrieve menu items'}), 500

@app.route('/api/check-auth', methods=['GET'])
def check_auth():
    try:
        if current_user.is_authenticated:
            return jsonify({
                'authenticated': True,
                'user': current_user.to_dict()
            }), 200
        return jsonify({'authenticated': False}), 401
    except Exception as e:
        logger.exception("Error checking authentication status")
        return jsonify({'error': 'Failed to check authentication status'}), 500

# Profile management route
@app.route('/api/profile', methods=['GET', 'PUT'])
@login_required
def profile():
    if request.method == 'GET':
        try:
            return jsonify(current_user.to_dict()), 200
        except Exception as e:
            logger.exception("Error retrieving user profile")
            return jsonify({'error': 'Failed to retrieve profile'}), 500

    elif request.method == 'PUT':
        try:
            data = request.get_json()
            user = current_user

            # Update allowed fields
            allowed_fields = ['first_name', 'last_name', 'phone_number']
            for field in allowed_fields:
                if field in data:
                    setattr(user, field, data[field])

            # Handle password update separately
            if 'current_password' in data and 'new_password' in data:
                if user.check_password_correction(data['current_password']):
                    user.password = data['new_password']
                else:
                    return jsonify({'error': 'Current password is incorrect'}), 400

            db.session.commit()
            logger.info(f"Profile updated for user: {user.email}")
            return jsonify({'message': 'Profile updated successfully'}), 200

        except Exception as e:
            logger.exception("Error updating user profile")
            db.session.rollback()
            return jsonify({'error': 'Failed to update profile'}), 500

# Error handlers
@app.errorhandler(404)
def not_found_error(error):
    return jsonify({'error': 'Resource not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return jsonify({'error': 'Internal server error'}), 500