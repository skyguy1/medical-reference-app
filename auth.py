"""
Authentication module for the medical reference app

This module provides user authentication and authorization functionality.
"""
from flask import Blueprint, request, jsonify, session, redirect, url_for, render_template, flash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User
import datetime
import jwt
import os

# Secret key for JWT
SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key')

# Create blueprint
auth = Blueprint('auth', __name__)

# Initialize login manager
login_manager = LoginManager()
login_manager.login_view = 'auth.login'

@login_manager.user_loader
def load_user(user_id):
    """Load user by ID"""
    return User.query.get(int(user_id))

@auth.route('/register', methods=['GET', 'POST'])
def register():
    """Register a new user"""
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        # Validate input
        if not username or not email or not password:
            flash('All fields are required', 'error')
            return render_template('register.html')
        
        # Check if user already exists
        if User.query.filter_by(username=username).first():
            flash('Username already exists', 'error')
            return render_template('register.html')
        
        if User.query.filter_by(email=email).first():
            flash('Email already registered', 'error')
            return render_template('register.html')
        
        # Create new user
        new_user = User(
            username=username,
            email=email,
            password=generate_password_hash(password, method='pbkdf2:sha256')
        )
        
        # Add user to database
        db.session.add(new_user)
        db.session.commit()
        
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('register.html')

@auth.route('/login', methods=['GET', 'POST'])
def login():
    """Log in a user"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False
        
        # Validate input
        if not username or not password:
            flash('Please provide username and password', 'error')
            return render_template('login.html')
        
        # Check if user exists
        user = User.query.filter_by(username=username).first()
        
        if not user or not check_password_hash(user.password, password):
            flash('Invalid username or password', 'error')
            return render_template('login.html')
        
        # Log in user
        login_user(user, remember=remember)
        
        # Update last login time
        user.last_login = datetime.datetime.utcnow()
        db.session.commit()
        
        return redirect(url_for('index'))
    
    return render_template('login.html')

@auth.route('/logout')
@login_required
def logout():
    """Log out a user"""
    logout_user()
    return redirect(url_for('index'))

@auth.route('/profile')
@login_required
def profile():
    """User profile page"""
    return render_template('profile.html', user=current_user)

@auth.route('/api/token', methods=['POST'])
def get_token():
    """Get JWT token for API access"""
    auth = request.authorization
    
    if not auth or not auth.username or not auth.password:
        return jsonify({'message': 'Authentication required'}), 401
    
    user = User.query.filter_by(username=auth.username).first()
    
    if not user or not check_password_hash(user.password, auth.password):
        return jsonify({'message': 'Invalid credentials'}), 401
    
    # Generate token
    token = jwt.encode({
        'user_id': user.id,
        'username': user.username,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
    }, SECRET_KEY, algorithm='HS256')
    
    return jsonify({'token': token})

def token_required(f):
    """Decorator for API endpoints that require token authentication"""
    def decorated(*args, **kwargs):
        token = None
        
        # Check if token is in headers
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            if auth_header.startswith('Bearer '):
                token = auth_header.split(' ')[1]
        
        if not token:
            return jsonify({'message': 'Token is missing'}), 401
        
        try:
            # Decode token
            data = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            current_user = User.query.filter_by(id=data['user_id']).first()
        except:
            return jsonify({'message': 'Invalid token'}), 401
        
        return f(current_user, *args, **kwargs)
    
    return decorated
