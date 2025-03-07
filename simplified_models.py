"""
Simplified database models for Medical Reference App
"""
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()

# Association tables
condition_specialty = db.Table('condition_specialty',
    db.Column('condition_id', db.Integer, db.ForeignKey('condition.id'), primary_key=True),
    db.Column('specialty_id', db.Integer, db.ForeignKey('specialty.id'), primary_key=True)
)

medication_condition = db.Table('medication_condition',
    db.Column('medication_id', db.Integer, db.ForeignKey('medication.id'), primary_key=True),
    db.Column('condition_id', db.Integer, db.ForeignKey('condition.id'), primary_key=True)
)

class User(UserMixin, db.Model):
    """User model for authentication"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.username}>'

class Condition(db.Model):
    """Medical condition model"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    symptoms = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    specialties = db.relationship('Specialty', secondary=condition_specialty, 
                                 backref=db.backref('conditions', lazy='dynamic'))
    medications = db.relationship('Medication', secondary=medication_condition,
                                 backref=db.backref('conditions', lazy='dynamic'))
    
    def __repr__(self):
        return f'<Condition {self.name}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'symptoms': self.symptoms,
            'specialties': [s.name for s in self.specialties],
            'medications': [m.name for m in self.medications],
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class Medication(db.Model):
    """Medication model"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    dosage = db.Column(db.String(100))
    side_effects = db.Column(db.Text)
    drug_class = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Medication {self.name}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'dosage': self.dosage,
            'side_effects': self.side_effects,
            'drug_class': self.drug_class,
            'conditions': [c.name for c in self.conditions],
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class Specialty(db.Model):
    """Medical specialty model"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Specialty {self.name}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'conditions': [c.name for c in self.conditions],
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class Reference(db.Model):
    """Medical reference model"""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    authors = db.Column(db.String(200))
    journal = db.Column(db.String(100))
    publication_date = db.Column(db.Date)
    doi = db.Column(db.String(100))
    abstract = db.Column(db.Text)
    url = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Reference {self.title}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'authors': self.authors,
            'journal': self.journal,
            'publication_date': self.publication_date.isoformat() if self.publication_date else None,
            'doi': self.doi,
            'abstract': self.abstract,
            'url': self.url,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class Guideline(db.Model):
    """Medical guideline model"""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    organization = db.Column(db.String(100))
    publication_date = db.Column(db.Date)
    summary = db.Column(db.Text)
    url = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Guideline {self.title}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'organization': self.organization,
            'publication_date': self.publication_date.isoformat() if self.publication_date else None,
            'summary': self.summary,
            'url': self.url,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

# Relationship model for medications
class MedicationRelationship(db.Model):
    """Model for medication interactions"""
    id = db.Column(db.Integer, primary_key=True)
    medication1_id = db.Column(db.Integer, db.ForeignKey('medication.id'))
    medication2_id = db.Column(db.Integer, db.ForeignKey('medication.id'))
    interaction_type = db.Column(db.String(100))
    description = db.Column(db.Text)
    severity = db.Column(db.String(50))
    
    medication1 = db.relationship('Medication', foreign_keys=[medication1_id])
    medication2 = db.relationship('Medication', foreign_keys=[medication2_id])
    
    def __repr__(self):
        return f'<MedicationRelationship {self.medication1_id} - {self.medication2_id}>'
