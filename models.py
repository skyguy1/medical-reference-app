from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin
from sqlalchemy import event

db = SQLAlchemy()

# Association tables for many-to-many relationships
condition_medication = db.Table('condition_medication',
    db.Column('condition_id', db.Integer, db.ForeignKey('condition.id'), primary_key=True),
    db.Column('medication_id', db.Integer, db.ForeignKey('medication.id'), primary_key=True)
)

condition_specialty = db.Table('condition_specialty',
    db.Column('condition_id', db.Integer, db.ForeignKey('condition.id'), primary_key=True),
    db.Column('specialty_id', db.Integer, db.ForeignKey('specialty.id'), primary_key=True)
)

medication_specialty = db.Table('medication_specialty',
    db.Column('medication_id', db.Integer, db.ForeignKey('medication.id'), primary_key=True),
    db.Column('specialty_id', db.Integer, db.ForeignKey('specialty.id'), primary_key=True)
)

condition_reference = db.Table('condition_reference',
    db.Column('condition_id', db.Integer, db.ForeignKey('condition.id'), primary_key=True),
    db.Column('reference_id', db.Integer, db.ForeignKey('reference.id'), primary_key=True)
)

medication_reference = db.Table('medication_reference',
    db.Column('medication_id', db.Integer, db.ForeignKey('medication.id'), primary_key=True),
    db.Column('reference_id', db.Integer, db.ForeignKey('reference.id'), primary_key=True)
)

# Global flag to disable history creation during database seeding
ENABLE_HISTORY_TRACKING = True

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    role = db.Column(db.String(20), default='user')  # 'user', 'editor', 'admin'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    is_active = db.Column(db.Boolean, default=True)
    is_admin = db.Column(db.Boolean, default=False)
    
    # Relationships
    favorites = db.relationship('Favorite', backref='user', lazy=True)
    
    def __repr__(self):
        return f'<User {self.username}>'
    
    def set_password(self, password):
        """Set password hash"""
        from werkzeug.security import generate_password_hash
        self.password = generate_password_hash(password)
        
    def check_password(self, password):
        """Check password hash"""
        from werkzeug.security import check_password_hash
        return check_password_hash(self.password, password)

class Favorite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    item_type = db.Column(db.String(20), nullable=False)  # 'condition', 'medication', etc.
    item_id = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Favorite {self.item_type}:{self.item_id} by User:{self.user_id}>'

class Condition(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text, nullable=False)
    symptoms = db.Column(db.Text)  # Stored as JSON string
    treatments = db.Column(db.Text)  # Stored as JSON string
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    version = db.Column(db.Integer, default=1)
    
    # Relationships
    medications = db.relationship('Medication', secondary=condition_medication, 
                                 backref=db.backref('conditions', lazy='dynamic'))
    specialty_id = db.Column(db.Integer, db.ForeignKey('specialty.id'))
    specialty = db.relationship('Specialty', backref=db.backref('conditions', lazy='dynamic'))
    references = db.relationship('Reference', secondary=condition_reference,
                               backref=db.backref('conditions', lazy='dynamic'))
    history = db.relationship('ConditionHistory', backref='current_condition', lazy='dynamic')
    
    def __repr__(self):
        return f'<Condition {self.name}>'
    
    def create_history_record(self):
        """Create a history record before updating"""
        if not ENABLE_HISTORY_TRACKING:
            return
        
        history = ConditionHistory(
            condition_id=self.id,
            name=self.name,
            description=self.description,
            symptoms=self.symptoms,
            treatments=self.treatments,
            version=self.version
        )
        db.session.add(history)
        self.version += 1

class ConditionHistory(db.Model):
    """History model for tracking changes to conditions"""
    __tablename__ = 'condition_history'
    
    id = db.Column(db.Integer, primary_key=True)
    condition_id = db.Column(db.Integer, db.ForeignKey('condition.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    symptoms = db.Column(db.Text)  # JSON string
    treatments = db.Column(db.Text)  # JSON string
    version = db.Column(db.Integer, nullable=False)
    changed_by_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    changed_at = db.Column(db.DateTime, default=datetime.utcnow)
    change_type = db.Column(db.String(20))  # 'create', 'update', 'delete'
    
    # Relationships
    condition = db.relationship('Condition', foreign_keys=[condition_id])
    changed_by = db.relationship('User')
    
    def __repr__(self):
        return f'<ConditionHistory {self.condition_id}-v{self.version}>'

def create_condition_history(condition, user_id=None, change_type='update'):
    """Create a history record for a condition"""
    if not ENABLE_HISTORY_TRACKING:
        return
        
    # Get the latest version number
    latest = ConditionHistory.query.filter_by(condition_id=condition.id).order_by(ConditionHistory.version.desc()).first()
    version = (latest.version + 1) if latest else 1
    
    history = ConditionHistory(
        condition_id=condition.id,
        name=condition.name,
        description=condition.description,
        symptoms=condition.symptoms,
        treatments=condition.treatments,
        version=version,
        changed_by_id=user_id,
        change_type=change_type
    )
    db.session.add(history)
    return history

@event.listens_for(Condition, 'after_update')
def condition_after_update(mapper, connection, condition):
    """Create history record after condition update"""
    if not db.session.is_active or not ENABLE_HISTORY_TRACKING:
        return
    create_condition_history(condition)

@event.listens_for(Condition, 'after_insert')
def condition_after_insert(mapper, connection, condition):
    """Create history record after condition insert"""
    if not db.session.is_active or not ENABLE_HISTORY_TRACKING:
        return
    create_condition_history(condition, change_type='create')

class Medication(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    class_name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)  # Adding description field
    uses = db.Column(db.Text)  # Stored as JSON string
    side_effects = db.Column(db.Text)  # Stored as JSON string
    dosing = db.Column(db.Text, nullable=False)
    contraindications = db.Column(db.Text)  # Stored as JSON string
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    version = db.Column(db.Integer, default=1)
    
    # Relationships
    specialties = db.relationship('Specialty', secondary=medication_specialty, 
                                 backref=db.backref('medications', lazy='dynamic'))
    references = db.relationship('Reference', secondary=medication_reference,
                               backref=db.backref('medications', lazy='dynamic'))
    history = db.relationship('MedicationHistory', backref='current_medication', lazy='dynamic')
    
    def __repr__(self):
        return f'<Medication {self.name}>'
    
    def create_history_record(self):
        """Create a history record before updating"""
        if not ENABLE_HISTORY_TRACKING:
            return
        
        history = MedicationHistory(
            medication_id=self.id,
            name=self.name,
            class_name=self.class_name,
            description=self.description,
            uses=self.uses,
            side_effects=self.side_effects,
            dosing=self.dosing,
            contraindications=self.contraindications,
            version=self.version
        )
        db.session.add(history)
        self.version += 1

class MedicationHistory(db.Model):
    """History model for tracking changes to medications"""
    __tablename__ = 'medication_history'
    
    id = db.Column(db.Integer, primary_key=True)
    medication_id = db.Column(db.Integer, db.ForeignKey('medication.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    class_name = db.Column(db.String(100))
    description = db.Column(db.Text)  # Adding description field
    uses = db.Column(db.Text)  # JSON string
    side_effects = db.Column(db.Text)  # JSON string
    dosing = db.Column(db.Text)
    contraindications = db.Column(db.Text)  # JSON string
    version = db.Column(db.Integer, nullable=False)
    changed_by_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    changed_at = db.Column(db.DateTime, default=datetime.utcnow)
    change_type = db.Column(db.String(20))  # 'create', 'update', 'delete'
    
    # Relationships
    medication = db.relationship('Medication', foreign_keys=[medication_id])
    changed_by = db.relationship('User')
    
    def __repr__(self):
        return f'<MedicationHistory {self.medication_id}-v{self.version}>'

def create_medication_history(medication, user_id=None, change_type='update'):
    """Create a history record for a medication"""
    if not ENABLE_HISTORY_TRACKING:
        return
        
    # Get the latest version number
    latest = MedicationHistory.query.filter_by(medication_id=medication.id).order_by(MedicationHistory.version.desc()).first()
    version = (latest.version + 1) if latest else 1
    
    history = MedicationHistory(
        medication_id=medication.id,
        name=medication.name,
        class_name=medication.class_name,
        description=medication.description,
        uses=medication.uses,
        side_effects=medication.side_effects,
        dosing=medication.dosing,
        contraindications=medication.contraindications,
        version=version,
        changed_by_id=user_id,
        change_type=change_type
    )
    db.session.add(history)
    return history

@event.listens_for(Medication, 'after_update')
def medication_after_update(mapper, connection, medication):
    """Create history record after medication update"""
    if not db.session.is_active or not ENABLE_HISTORY_TRACKING:
        return
    create_medication_history(medication)

@event.listens_for(Medication, 'after_insert')
def medication_after_insert(mapper, connection, medication):
    """Create history record after medication insert"""
    if not db.session.is_active or not ENABLE_HISTORY_TRACKING:
        return
    create_medication_history(medication, change_type='create')

class MedicationRelationship(db.Model):
    """Model for relationships between medications"""
    __tablename__ = 'medication_relationships'
    
    id = db.Column(db.Integer, primary_key=True)
    medication_id = db.Column(db.Integer, db.ForeignKey('medication.id'), nullable=False)
    related_medication_id = db.Column(db.Integer, db.ForeignKey('medication.id'), nullable=False)
    relationship_type = db.Column(db.String(50), nullable=False)  # e.g., "same_class", "alternative", "complementary"
    
    # Define relationships
    medication = db.relationship('Medication', foreign_keys=[medication_id], backref=db.backref('related_to', lazy='dynamic'))
    related_medication = db.relationship('Medication', foreign_keys=[related_medication_id], backref=db.backref('related_from', lazy='dynamic'))
    
    def __repr__(self):
        return f'<MedicationRelationship {self.medication_id} -> {self.related_medication_id} ({self.relationship_type})>'

class Specialty(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Specialty {self.name}>'

class Reference(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    authors = db.Column(db.String(200))
    publication = db.Column(db.String(200))
    year = db.Column(db.Integer)
    url = db.Column(db.String(500))
    doi = db.Column(db.String(100))
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Reference {self.title}>'

class Guideline(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    organization = db.Column(db.String(200), nullable=False)
    publication_year = db.Column(db.Integer, nullable=False)
    url = db.Column(db.String(500))
    summary = db.Column(db.Text)
    specialty_id = db.Column(db.Integer, db.ForeignKey('specialty.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    version = db.Column(db.Integer, default=1)
    
    # Relationships
    specialty = db.relationship('Specialty', backref=db.backref('guidelines', lazy='dynamic'))
    history = db.relationship('GuidelineHistory', backref='current_guideline', lazy='dynamic')
    
    def __repr__(self):
        return f'<Guideline {self.title}>'
    
    def create_history_record(self):
        """Create a history record before updating"""
        if not ENABLE_HISTORY_TRACKING:
            return
        
        history = GuidelineHistory(
            guideline_id=self.id,
            title=self.title,
            organization=self.organization,
            publication_year=self.publication_year,
            url=self.url,
            summary=self.summary,
            version=self.version
        )
        db.session.add(history)
        self.version += 1

class GuidelineHistory(db.Model):
    """History model for tracking changes to guidelines"""
    __tablename__ = 'guideline_history'
    
    id = db.Column(db.Integer, primary_key=True)
    guideline_id = db.Column(db.Integer, db.ForeignKey('guideline.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    organization = db.Column(db.String(100))
    publication_year = db.Column(db.Integer)
    summary = db.Column(db.Text)
    url = db.Column(db.String(255))
    version = db.Column(db.Integer, nullable=False)
    changed_by_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    changed_at = db.Column(db.DateTime, default=datetime.utcnow)
    change_type = db.Column(db.String(20))  # 'create', 'update', 'delete'
    
    # Relationships
    guideline = db.relationship('Guideline', foreign_keys=[guideline_id])
    changed_by = db.relationship('User')
    
    def __repr__(self):
        return f'<GuidelineHistory {self.guideline_id}-v{self.version}>'

def create_guideline_history(guideline, user_id=None, change_type='update'):
    """Create a history record for a guideline"""
    if not ENABLE_HISTORY_TRACKING:
        return
        
    # Get the latest version number
    latest = GuidelineHistory.query.filter_by(guideline_id=guideline.id).order_by(GuidelineHistory.version.desc()).first()
    version = (latest.version + 1) if latest else 1
    
    history = GuidelineHistory(
        guideline_id=guideline.id,
        title=guideline.title,
        organization=guideline.organization,
        publication_year=guideline.publication_year,
        summary=guideline.summary,
        url=guideline.url,
        version=version,
        changed_by_id=user_id,
        change_type=change_type
    )
    db.session.add(history)
    return history

@event.listens_for(Guideline, 'after_update')
def guideline_after_update(mapper, connection, guideline):
    """Create history record after guideline update"""
    if not db.session.is_active or not ENABLE_HISTORY_TRACKING:
        return
    create_guideline_history(guideline)

@event.listens_for(Guideline, 'after_insert')
def guideline_after_insert(mapper, connection, guideline):
    """Create history record after guideline insert"""
    if not db.session.is_active or not ENABLE_HISTORY_TRACKING:
        return
    create_guideline_history(guideline, change_type='create')
