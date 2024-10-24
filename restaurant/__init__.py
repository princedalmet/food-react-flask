from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_cors import CORS
import os

# Initialize Flask app
app = Flask(__name__)

# Load configuration from config.py
app.config.from_pyfile('../config.py')

# Initialize extensions
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"  # Change to 'login'
migrate = Migrate(app, db)

# Delay importing User model until after app initialization
@login_manager.user_loader
def load_user(user_id):
    from restaurant.models import User  # Import here to avoid circular import
    return User.query.get(int(user_id))

# Allow CORS to enable communication between React (frontend) and Flask (backend)
CORS(app)

# Import routes after initializing extensions to prevent circular import
from restaurant import routes
