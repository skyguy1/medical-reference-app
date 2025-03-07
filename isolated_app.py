"""
Direct implementation of the Medical Reference App
This file directly implements the essential functionality without dependencies
"""
import os
import sys
from flask import Flask, render_template, redirect, url_for, request, flash, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from datetime import datetime

# Create Flask app
app = Flask(__name__, template_folder='standalone/templates', static_folder='standalone/static')

# Configure the app
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-key-for-testing')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///medical_reference.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Define models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    email = db.Column(db.String(120), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean, default=False)
    notes = db.relationship('Note', backref='author', lazy='dynamic')
    favorites = db.relationship('Favorite', backref='user', lazy='dynamic')
    specialty_notifications = db.Column(db.Boolean, default=False)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Specialty(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text)
    conditions = db.relationship('Condition', secondary='specialty_condition', backref='specialties')
    medications = db.relationship('Medication', secondary='specialty_medication', backref='specialties')
    guidelines = db.relationship('Guideline', secondary='specialty_guideline', backref='specialties')
    
    def __repr__(self):
        return f'<Specialty {self.name}>'

class Medication(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    generic_name = db.Column(db.String(100))
    drug_class = db.Column(db.String(100))
    description = db.Column(db.Text)
    dosage = db.Column(db.String(100))
    side_effects = db.Column(db.Text)
    contraindications = db.Column(db.Text)
    notes = db.relationship('Note', backref='medication', lazy='dynamic')
    favorites = db.relationship('Favorite', backref='medication', lazy='dynamic')
    conditions = db.relationship('Condition', secondary='medication_condition', backref='medications')
    guidelines = db.relationship('Guideline', secondary='medication_guideline', backref='medications')
    
    def __repr__(self):
        return f'<Medication {self.name}>'

class Condition(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    symptoms = db.Column(db.Text)
    diagnosis = db.Column(db.Text)
    treatment = db.Column(db.Text)
    notes = db.relationship('Note', backref='condition', lazy='dynamic')
    favorites = db.relationship('Favorite', backref='condition', lazy='dynamic')
    guidelines = db.relationship('Guideline', secondary='condition_guideline', backref='conditions')
    
    def __repr__(self):
        return f'<Condition {self.name}>'

class Guideline(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text)
    source = db.Column(db.String(200))
    publication_date = db.Column(db.Date)
    summary = db.Column(db.Text)
    evidence_level = db.Column(db.String(50))
    recommendations = db.Column(db.Text)
    
    def __repr__(self):
        return f'<Guideline {self.title}>'

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    medication_id = db.Column(db.Integer, db.ForeignKey('medication.id'))
    condition_id = db.Column(db.Integer, db.ForeignKey('condition.id'))

class Favorite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    medication_id = db.Column(db.Integer, db.ForeignKey('medication.id'))
    condition_id = db.Column(db.Integer, db.ForeignKey('condition.id'))

# Association tables
specialty_condition = db.Table('specialty_condition',
    db.Column('specialty_id', db.Integer, db.ForeignKey('specialty.id'), primary_key=True),
    db.Column('condition_id', db.Integer, db.ForeignKey('condition.id'), primary_key=True)
)

specialty_medication = db.Table('specialty_medication',
    db.Column('specialty_id', db.Integer, db.ForeignKey('specialty.id'), primary_key=True),
    db.Column('medication_id', db.Integer, db.ForeignKey('medication.id'), primary_key=True)
)

specialty_guideline = db.Table('specialty_guideline',
    db.Column('specialty_id', db.Integer, db.ForeignKey('specialty.id'), primary_key=True),
    db.Column('guideline_id', db.Integer, db.ForeignKey('guideline.id'), primary_key=True)
)

medication_condition = db.Table('medication_condition',
    db.Column('medication_id', db.Integer, db.ForeignKey('medication.id'), primary_key=True),
    db.Column('condition_id', db.Integer, db.ForeignKey('condition.id'), primary_key=True)
)

medication_guideline = db.Table('medication_guideline',
    db.Column('medication_id', db.Integer, db.ForeignKey('medication.id'), primary_key=True),
    db.Column('guideline_id', db.Integer, db.ForeignKey('guideline.id'), primary_key=True)
)

condition_guideline = db.Table('condition_guideline',
    db.Column('condition_id', db.Integer, db.ForeignKey('condition.id'), primary_key=True),
    db.Column('guideline_id', db.Integer, db.ForeignKey('guideline.id'), primary_key=True)
)

user_specialty = db.Table('user_specialty',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('specialty_id', db.Integer, db.ForeignKey('specialty.id'), primary_key=True)
)

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        if User.query.filter_by(username=username).first():
            flash('Username already exists')
            return redirect(url_for('register'))
        
        if User.query.filter_by(email=email).first():
            flash('Email already registered')
            return redirect(url_for('register'))
        
        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        
        flash('Registration successful!')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        remember = 'remember' in request.form
        
        user = User.query.filter_by(username=username).first()
        
        if not user or not user.check_password(password):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        
        login_user(user, remember=remember)
        return redirect(url_for('index'))
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/medications')
def medications():
    medications = Medication.query.all()
    return render_template('medications.html', medications=medications)

@app.route('/medications/<int:id>')
def medication_detail(id):
    medication = Medication.query.get_or_404(id)
    return render_template('medication_detail.html', medication=medication)

@app.route('/conditions')
def conditions():
    conditions = Condition.query.all()
    return render_template('conditions.html', conditions=conditions)

@app.route('/conditions/<int:id>')
def condition_detail(id):
    condition = Condition.query.get_or_404(id)
    return render_template('condition_detail.html', condition=condition)

@app.route('/specialties')
def specialties():
    specialties = Specialty.query.all()
    return render_template('specialties.html', specialties=specialties)

@app.route('/specialties/<int:id>')
def specialty_detail(id):
    specialty = Specialty.query.get_or_404(id)
    return render_template('specialty_detail.html', specialty=specialty)

@app.route('/guidelines')
def guidelines():
    guidelines = Guideline.query.all()
    return render_template('guidelines.html', guidelines=guidelines)

@app.route('/guidelines/<int:id>')
def guideline_detail(id):
    guideline = Guideline.query.get_or_404(id)
    return render_template('guideline_detail.html', guideline=guideline)

@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html')

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        current_password = request.form.get('current_password')
        
        if not current_user.check_password(current_password):
            flash('Current password is incorrect')
            return redirect(url_for('edit_profile'))
        
        if username != current_user.username and User.query.filter_by(username=username).first():
            flash('Username already exists')
            return redirect(url_for('edit_profile'))
        
        if email != current_user.email and User.query.filter_by(email=email).first():
            flash('Email already registered')
            return redirect(url_for('edit_profile'))
        
        current_user.username = username
        current_user.email = email
        
        new_password = request.form.get('new_password')
        if new_password:
            current_user.set_password(new_password)
        
        db.session.commit()
        flash('Profile updated successfully')
        return redirect(url_for('profile'))
    
    return render_template('edit_profile.html')

@app.route('/admin')
@login_required
def admin():
    if not current_user.is_admin:
        flash('You do not have permission to access this page')
        return redirect(url_for('index'))
    
    users = User.query.all()
    return render_template('admin.html', users=users)

@app.route('/health')
def health():
    """Health check endpoint for Render"""
    return jsonify({"status": "healthy"})

# This is the only entry point for the application
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
