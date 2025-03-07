"""
Authentication module for Medical Reference App
"""
from flask import Blueprint, render_template_string, redirect, url_for, flash, request, session
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash
import logging
from models import db, User

# Configure logging
logger = logging.getLogger(__name__)

# Create Blueprint
auth_bp = Blueprint('auth', __name__)

# Login Manager
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Please log in to access this page.'

@login_manager.user_loader
def load_user(user_id):
    """Load user by ID"""
    return User.query.get(int(user_id))

# Login template
LOGIN_TEMPLATE = """
<h2>Login</h2>
<div class="card">
    {% if error %}
    <p class="error">{{ error }}</p>
    {% endif %}
    
    <form method="POST" action="{{ url_for('auth.login') }}">
        <div style="margin-bottom: 15px;">
            <label for="username">Username:</label>
            <input type="text" id="username" name="username" required style="width: 100%; padding: 8px; margin-top: 5px;">
        </div>
        
        <div style="margin-bottom: 15px;">
            <label for="password">Password:</label>
            <input type="password" id="password" name="password" required style="width: 100%; padding: 8px; margin-top: 5px;">
        </div>
        
        <div style="margin-bottom: 15px;">
            <label>
                <input type="checkbox" name="remember"> Remember me
            </label>
        </div>
        
        <button type="submit" class="button">Login</button>
    </form>
    
    <p style="margin-top: 15px;">
        Don't have an account? <a href="{{ url_for('auth.register') }}">Register</a>
    </p>
</div>
"""

# Register template
REGISTER_TEMPLATE = """
<h2>Register</h2>
<div class="card">
    {% if error %}
    <p class="error">{{ error }}</p>
    {% endif %}
    
    <form method="POST" action="{{ url_for('auth.register') }}">
        <div style="margin-bottom: 15px;">
            <label for="username">Username:</label>
            <input type="text" id="username" name="username" required style="width: 100%; padding: 8px; margin-top: 5px;">
        </div>
        
        <div style="margin-bottom: 15px;">
            <label for="email">Email:</label>
            <input type="email" id="email" name="email" required style="width: 100%; padding: 8px; margin-top: 5px;">
        </div>
        
        <div style="margin-bottom: 15px;">
            <label for="password">Password:</label>
            <input type="password" id="password" name="password" required style="width: 100%; padding: 8px; margin-top: 5px;">
        </div>
        
        <div style="margin-bottom: 15px;">
            <label for="confirm_password">Confirm Password:</label>
            <input type="password" id="confirm_password" name="confirm_password" required style="width: 100%; padding: 8px; margin-top: 5px;">
        </div>
        
        <button type="submit" class="button">Register</button>
    </form>
    
    <p style="margin-top: 15px;">
        Already have an account? <a href="{{ url_for('auth.login') }}">Login</a>
    </p>
</div>
"""

# Profile template
PROFILE_TEMPLATE = """
<h2>User Profile</h2>
<div class="card">
    <h3>Welcome, {{ current_user.username }}!</h3>
    
    <table>
        <tr>
            <th>Username</th>
            <td>{{ current_user.username }}</td>
        </tr>
        <tr>
            <th>Email</th>
            <td>{{ current_user.email }}</td>
        </tr>
        <tr>
            <th>User ID</th>
            <td>{{ current_user.id }}</td>
        </tr>
    </table>
    
    <a href="{{ url_for('auth.logout') }}" class="button" style="margin-top: 15px;">Logout</a>
</div>
"""

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Login route"""
    error = None
    
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        remember = 'remember' in request.form
        
        user = User.query.filter_by(username=username).first()
        
        if not user or not user.check_password(password):
            error = 'Invalid username or password'
        else:
            login_user(user, remember=remember)
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            return redirect(url_for('index'))
    
    return render_template_string(
        session.get('base_template', '{{ content | safe }}'),
        content=render_template_string(LOGIN_TEMPLATE, error=error)
    )

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """Register route"""
    error = None
    
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        # Validate input
        if not username or not email or not password:
            error = 'All fields are required'
        elif password != confirm_password:
            error = 'Passwords do not match'
        elif User.query.filter_by(username=username).first():
            error = 'Username already exists'
        elif User.query.filter_by(email=email).first():
            error = 'Email already registered'
        else:
            # Create new user
            user = User(username=username, email=email)
            user.set_password(password)
            
            try:
                db.session.add(user)
                db.session.commit()
                login_user(user)
                return redirect(url_for('index'))
            except Exception as e:
                db.session.rollback()
                logger.error(f"Error creating user: {e}")
                error = f"Error creating user: {str(e)}"
    
    return render_template_string(
        session.get('base_template', '{{ content | safe }}'),
        content=render_template_string(REGISTER_TEMPLATE, error=error)
    )

@auth_bp.route('/logout')
@login_required
def logout():
    """Logout route"""
    logout_user()
    return redirect(url_for('index'))

@auth_bp.route('/profile')
@login_required
def profile():
    """User profile route"""
    return render_template_string(
        session.get('base_template', '{{ content | safe }}'),
        content=render_template_string(PROFILE_TEMPLATE)
    )

def create_admin_user(app):
    """Create admin user if it doesn't exist"""
    with app.app_context():
        if User.query.filter_by(username='admin').first() is None:
            admin = User(
                username='admin',
                email='admin@example.com'
            )
            admin.set_password('admin')
            db.session.add(admin)
            db.session.commit()
            logger.info("Admin user created")
