from restaurant import db, bcrypt
from flask_login import UserMixin
from datetime import datetime

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer(), primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    phone_number = db.Column(db.String(15), nullable=True)
    role = db.Column(db.String(20), nullable=False, default='customer')
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    
    # Relationship with orders
    orders = db.relationship('Item', backref='customer', lazy=True, 
                           foreign_keys='Item.orderer')

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if 'password' in kwargs:
            self.password = kwargs['password']

    @property
    def password(self):
        raise AttributeError('Password is not readable')

    @password.setter
    def password(self, plain_text_password):
        if plain_text_password:
            self.password_hash = bcrypt.generate_password_hash(
                plain_text_password
            ).decode('utf-8')

    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)

    def update_last_login(self):
        """Update the last login timestamp"""
        self.last_login = datetime.utcnow()
        db.session.commit()

    @property
    def full_name(self):
        """Return the user's full name"""
        return f"{self.first_name} {self.last_name}"

    def to_dict(self):
        """Convert user object to dictionary for API responses"""
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'phone_number': self.phone_number,
            'role': self.role
        }

    def __repr__(self):
        return f'<User {self.email}>'

class Item(db.Model):
    __tablename__ = 'item'
    item_id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=30), nullable=False)
    description = db.Column(db.String(length=50), nullable=False)
    price = db.Column(db.Integer(), nullable=False)
    source = db.Column(db.String(length=30), nullable=False)
    orderer = db.Column(db.Integer(), db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

    def to_dict(self):
        """Convert item object to dictionary for API responses"""
        return {
            'item_id': self.item_id,
            'name': self.name,
            'description': self.description,
            'price': self.price,
            'source': self.source
        }

    def __repr__(self):
        return f'<Item {self.name}>'