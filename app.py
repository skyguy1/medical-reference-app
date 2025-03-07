from flask import Flask, render_template, request, jsonify, send_file, url_for, redirect, flash
import json
import os
import logging
from flask_migrate import Migrate
from flask_login import LoginManager, login_required, current_user
from datetime import datetime
from models import db, Condition, Medication, Specialty, Reference, Guideline, User, MedicationRelationship
from utils import safe_json_loads
import auth
from auth import login_manager
from api import api
from cache import cache_result, clear_expired_cache
from visualizations import (
    get_specialty_distribution, 
    get_medication_class_distribution,
    get_condition_network,
    get_reference_timeline,
    get_guideline_organization_distribution,
    get_condition_symptom_heatmap
)
from export import (
    export_conditions,
    export_medications,
    export_specialties,
    export_references,
    export_guidelines,
    export_all
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
# Get database URL from environment variable or use SQLite as fallback
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///medical_reference.db')
# Fix for Render's PostgreSQL URL format
if app.config['SQLALCHEMY_DATABASE_URI'] and app.config['SQLALCHEMY_DATABASE_URI'].startswith("postgres://"):
    app.config['SQLALCHEMY_DATABASE_URI'] = app.config['SQLALCHEMY_DATABASE_URI'].replace("postgres://", "postgresql://", 1)
    
logger.info(f"Using database: {app.config['SQLALCHEMY_DATABASE_URI']}")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')
app.config['CACHE_DIR'] = 'cache'

# Initialize the database
db.init_app(app)
migrate = Migrate(app, db)

# Register blueprints
app.register_blueprint(api, url_prefix='/api')
app.register_blueprint(auth.auth, url_prefix='/auth')

# Initialize login manager
login_manager.init_app(app)

# Ensure directories exist
os.makedirs('data', exist_ok=True)
os.makedirs('cache', exist_ok=True)
os.makedirs('exports', exist_ok=True)

@app.before_request
def before_request_func():
    """Clear expired cache before each request"""
    clear_expired_cache()
    return None

def seed_database():
    """Seed the database with initial data"""
    with app.app_context():
        # Create tables if they don't exist
        db.create_all()
        
        # Check if database is already seeded
        if Condition.query.count() > 0:
            print("Database already seeded. Skipping...")
            return
        
        print("Seeding database with medical data...")
        
        # Import data using the data importers
        try:
            # Disable history tracking during seeding to prevent SQLAlchemy errors
            from models import ENABLE_HISTORY_TRACKING
            import models
            models.ENABLE_HISTORY_TRACKING = False
            print("History tracking disabled during database seeding")
            
            # Import cardiology data (from hardcoded MEDICAL_DATA)
            print("Importing cardiology data...")
            from data_importer_cardiology import CardiologyDataImporter
            cardiology_importer = CardiologyDataImporter()
            cardiology_importer.import_data()
            
            # Import data from specialized importers
            print("Importing psychiatry data...")
            from data_importer_psychiatry import PsychiatryDataImporter
            psychiatry_importer = PsychiatryDataImporter()
            psychiatry_importer.import_data()
            
            print("Importing infectious diseases data...")
            from data_importer_infectious import InfectiousDataImporter
            infectious_importer = InfectiousDataImporter()
            infectious_importer.import_data()
            
            print("Importing rheumatology data...")
            from data_importer_rheumatology import RheumatologyDataImporter
            rheumatology_importer = RheumatologyDataImporter()
            rheumatology_importer.import_data()
            
            # Commit all changes
            db.session.commit()
            
            # Re-enable history tracking
            models.ENABLE_HISTORY_TRACKING = True
            print("History tracking re-enabled")
            
            print("Database seeding completed successfully!")
            
        except Exception as e:
            db.session.rollback()
            print(f"Error seeding database: {str(e)}")
            # Log the error
            with open('error_log.txt', 'a') as f:
                f.write(f"{datetime.now()}: Error seeding database: {str(e)}\n")
            # Re-enable history tracking in case of error
            import models
            models.ENABLE_HISTORY_TRACKING = True

@app.route('/')
def index():
    """Render the home page"""
    conditions = Condition.query.order_by(Condition.name).limit(5).all()
    medications = Medication.query.order_by(Medication.name).limit(5).all()
    specialties = Specialty.query.order_by(Specialty.name).all()
    return render_template('index.html', conditions=conditions, medications=medications, specialties=specialties)

@app.route('/search')
@cache_result(expiration=300)  # Cache results for 5 minutes
def search():
    """Search for conditions, medications, and specialties"""
    query = request.args.get('q', '')
    category = request.args.get('category', 'all')
    specialty = request.args.get('specialty', 'all')
    medication_class = request.args.get('class', 'all')
    
    if not query:
        # Get filter options for the search form
        specialties = Specialty.query.order_by(Specialty.name).all()
        medication_classes = db.session.query(Medication.class_name).distinct().order_by(Medication.class_name).all()
        return render_template('search.html', results=None, query=None, 
                              specialties=specialties, medication_classes=medication_classes,
                              selected_category=category, selected_specialty=specialty, 
                              selected_class=medication_class)
    
    # Base queries
    condition_query = Condition.query
    medication_query = Medication.query
    specialty_query = Specialty.query
    reference_query = Reference.query
    guideline_query = Guideline.query
    
    # Apply specialty filter if specified
    if specialty != 'all':
        condition_query = condition_query.join(Condition.specialty).filter(Specialty.name == specialty)
        medication_query = medication_query.join(Medication.specialties).filter(Specialty.name == specialty)
    
    # Apply medication class filter if specified
    if medication_class != 'all':
        medication_query = medication_query.filter(Medication.class_name == medication_class)
    
    # Search in conditions
    if category in ['all', 'conditions']:
        conditions = condition_query.filter(Condition.name.ilike(f'%{query}%') | 
                                          Condition.description.ilike(f'%{query}%')).all()
    else:
        conditions = []
    
    # Search in medications with enhanced description search
    if category in ['all', 'medications']:
        medications = medication_query.filter(
            Medication.name.ilike(f'%{query}%') | 
            Medication.class_name.ilike(f'%{query}%') |
            Medication.description.ilike(f'%{query}%') |
            Medication.uses.ilike(f'%{query}%') |
            Medication.dosing.ilike(f'%{query}%')
        ).all()
    else:
        medications = []
    
    # Search in specialties
    if category in ['all', 'specialties']:
        specialties_results = specialty_query.filter(Specialty.name.ilike(f'%{query}%') | 
                                           Specialty.description.ilike(f'%{query}%')).all()
    else:
        specialties_results = []
    
    # Search in references
    if category in ['all', 'references']:
        references = reference_query.filter(Reference.title.ilike(f'%{query}%') | 
                                          Reference.authors.ilike(f'%{query}%')).all()
    else:
        references = []
    
    # Search in guidelines
    if category in ['all', 'guidelines']:
        guidelines = guideline_query.filter(Guideline.title.ilike(f'%{query}%') | 
                                          Guideline.organization.ilike(f'%{query}%') |
                                          Guideline.summary.ilike(f'%{query}%')).all()
    else:
        guidelines = []
    
    # Combine results
    results = {
        'conditions': conditions,
        'medications': medications,
        'specialties': specialties_results,
        'references': references,
        'guidelines': guidelines
    }
    
    # Get filter options for the search form
    all_specialties = Specialty.query.order_by(Specialty.name).all()
    all_medication_classes = db.session.query(Medication.class_name).distinct().order_by(Medication.class_name).all()
    
    # Log search query with filters
    logger.info(f"Search query: {query} - Category: {category} - Specialty: {specialty} - Class: {medication_class} - " +
                f"Results: {len(conditions)} conditions, {len(medications)} medications, {len(specialties_results)} specialties, " +
                f"{len(references)} references, {len(guidelines)} guidelines")
    
    return render_template('search.html', results=results, query=query,
                          specialties=all_specialties, medication_classes=all_medication_classes,
                          selected_category=category, selected_specialty=specialty, 
                          selected_class=medication_class)

@app.route('/browse')
def browse():
    """Browse all conditions, medications, and specialties"""
    category = request.args.get('category', 'conditions')
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    specialty_filter = request.args.get('specialty', 'all')
    class_filter = request.args.get('class', 'all')
    
    # Get all specialties and medication classes for filter dropdowns
    all_specialties = Specialty.query.order_by(Specialty.name).all()
    all_medication_classes = db.session.query(Medication.class_name).distinct().order_by(Medication.class_name).all()
    
    if category == 'conditions':
        # Apply specialty filter if specified
        if specialty_filter != 'all':
            query = Condition.query.join(Condition.specialty).filter(Specialty.name == specialty_filter)
        else:
            query = Condition.query
            
        items = query.order_by(Condition.name).paginate(page=page, per_page=per_page)
        template = 'condition_list.html'
        
    elif category == 'medications':
        # Start with base query
        query = Medication.query
        
        # Apply specialty filter if specified
        if specialty_filter != 'all':
            query = query.join(Medication.specialties).filter(Specialty.name == specialty_filter)
            
        # Apply class filter if specified
        if class_filter != 'all':
            query = query.filter(Medication.class_name == class_filter)
            
        items = query.order_by(Medication.name).paginate(page=page, per_page=per_page)
        template = 'medication_list.html'
        
    elif category == 'specialties':
        items = Specialty.query.order_by(Specialty.name).paginate(page=page, per_page=per_page)
        template = 'specialty_list.html'
        
    elif category == 'references':
        items = Reference.query.order_by(Reference.title).paginate(page=page, per_page=per_page)
        template = 'reference_list.html'
        
    elif category == 'guidelines':
        items = Guideline.query.order_by(Guideline.title).paginate(page=page, per_page=per_page)
        template = 'guideline_list.html'
        
    else:
        return redirect(url_for('browse', category='conditions'))
    
    return render_template(template, 
                          items=items, 
                          category=category, 
                          specialties=all_specialties,
                          medication_classes=all_medication_classes,
                          specialty_filter=specialty_filter,
                          class_filter=class_filter)

@app.route('/condition/<int:condition_id>')
@cache_result(expiration=3600)  # Cache for 1 hour
def condition_detail(condition_id):
    """Display details for a specific condition"""
    condition = Condition.query.get_or_404(condition_id)
    
    # Parse JSON strings
    symptoms = safe_json_loads(condition.symptoms, [])
    treatments = safe_json_loads(condition.treatments, [])
    
    # Get related medications
    medications = condition.medications
    
    # Get related references
    references = condition.references
    
    return render_template('condition.html', 
                          condition=condition, 
                          symptoms=symptoms, 
                          treatments=treatments,
                          medications=medications,
                          references=references)

@app.route('/condition/<string:condition_name>')
@cache_result(expiration=3600)  # Cache for 1 hour
def condition_detail_by_name(condition_name):
    """Display details for a specific condition by name"""
    condition = Condition.query.filter_by(name=condition_name).first_or_404()
    
    # Parse JSON strings
    symptoms = safe_json_loads(condition.symptoms, [])
    treatments = safe_json_loads(condition.treatments, [])
    
    # Get related medications
    medications = condition.medications
    
    # Get related references
    references = condition.references
    
    return render_template('condition.html', 
                          condition=condition, 
                          symptoms=symptoms, 
                          treatments=treatments,
                          medications=medications,
                          references=references)

@app.route('/medication/<int:medication_id>')
@cache_result(expiration=3600)  # Cache for 1 hour
def medication_detail(medication_id):
    """Display details for a specific medication"""
    medication = Medication.query.get_or_404(medication_id)
    
    # Parse JSON strings
    uses = safe_json_loads(medication.uses, [])
    side_effects = safe_json_loads(medication.side_effects, [])
    contraindications = safe_json_loads(medication.contraindications, [])
    
    # Get related conditions
    conditions = medication.conditions
    
    # Get references
    references = medication.references
    
    # Get related medications
    related_medications = MedicationRelationship.query.filter_by(medication_id=medication_id).all()
    
    return render_template('medication.html', 
                          medication=medication, 
                          uses=uses, 
                          side_effects=side_effects, 
                          contraindications=contraindications,
                          conditions=conditions,
                          references=references,
                          related_medications=related_medications)

@app.route('/medication/<string:medication_name>')
@cache_result(expiration=3600)  # Cache for 1 hour
def medication_detail_by_name(medication_name):
    """Display details for a specific medication by name"""
    medication = Medication.query.filter_by(name=medication_name).first_or_404()
    
    # Parse JSON strings
    uses = safe_json_loads(medication.uses, [])
    side_effects = safe_json_loads(medication.side_effects, [])
    contraindications = safe_json_loads(medication.contraindications, [])
    
    # Get related conditions
    conditions = medication.conditions
    
    # Get references
    references = medication.references
    
    # Get related medications
    related_medications = MedicationRelationship.query.filter_by(medication_id=medication.id).all()
    
    return render_template('medication.html', 
                          medication=medication, 
                          uses=uses, 
                          side_effects=side_effects, 
                          contraindications=contraindications,
                          conditions=conditions,
                          references=references,
                          related_medications=related_medications)

@app.route('/preview/<string:medication_name>')
def preview_medication(medication_name):
    """Simple redirect to medication page for testing"""
    return redirect(url_for('medication_detail_by_name', medication_name=medication_name))

@app.route('/specialty/<int:specialty_id>')
@cache_result(expiration=3600)  # Cache for 1 hour
def specialty_detail(specialty_id):
    """Display details for a specific specialty"""
    specialty = Specialty.query.get_or_404(specialty_id)
    conditions = specialty.conditions.all()
    medications = specialty.medications.all()
    guidelines = specialty.guidelines.all()
    
    return render_template('specialty.html', 
                          specialty=specialty, 
                          conditions=conditions,
                          medications=medications,
                          guidelines=guidelines)

@app.route('/specialty/<string:specialty_name>')
@cache_result(expiration=3600)  # Cache for 1 hour
def specialty_detail_by_name(specialty_name):
    """Display details for a specific specialty by name"""
    specialty = Specialty.query.filter_by(name=specialty_name).first_or_404()
    conditions = specialty.conditions.all()
    medications = specialty.medications.all()
    guidelines = specialty.guidelines.all()
    
    return render_template('specialty.html', 
                          specialty=specialty, 
                          conditions=conditions,
                          medications=medications,
                          guidelines=guidelines)

@app.route('/reference/<int:reference_id>')
@cache_result(expiration=3600)  # Cache for 1 hour
def reference_detail(reference_id):
    """Display details for a specific reference"""
    reference = Reference.query.get_or_404(reference_id)
    return render_template('reference.html', reference=reference)

@app.route('/guideline/<int:guideline_id>')
@cache_result(expiration=3600)  # Cache for 1 hour
def guideline_detail(guideline_id):
    """Display details for a specific guideline"""
    guideline = Guideline.query.get_or_404(guideline_id)
    return render_template('guideline.html', guideline=guideline)

@app.route('/visualizations')
@login_required
def visualizations():
    """Display data visualizations"""
    # Get counts for overview
    condition_count = Condition.query.count()
    medication_count = Medication.query.count()
    specialty_count = Specialty.query.count()
    reference_count = Reference.query.count()
    
    # Get visualization data
    specialty_distribution = get_specialty_distribution()
    medication_class_distribution = get_medication_class_distribution()
    condition_network = get_condition_network()
    reference_timeline = get_reference_timeline()
    guideline_organization_distribution = get_guideline_organization_distribution()
    condition_symptom_heatmap = get_condition_symptom_heatmap()
    
    return render_template('visualizations.html',
                          condition_count=condition_count,
                          medication_count=medication_count,
                          specialty_count=specialty_count,
                          reference_count=reference_count,
                          specialty_distribution=specialty_distribution,
                          medication_class_distribution=medication_class_distribution,
                          condition_network=condition_network,
                          reference_timeline=reference_timeline,
                          guideline_organization_distribution=guideline_organization_distribution,
                          condition_symptom_heatmap=condition_symptom_heatmap)

@app.route('/export')
@login_required
def export():
    """Export data page"""
    return render_template('export.html')

@app.route('/export/download')
@login_required
def export_download():
    """Download exported data"""
    data_type = request.args.get('type', 'all')
    format = request.args.get('format', 'json')
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"{data_type}_{timestamp}"
    
    try:
        if data_type == 'conditions':
            file_path = export_conditions(format=format, filename=filename)
        elif data_type == 'medications':
            file_path = export_medications(format=format, filename=filename)
        elif data_type == 'specialties':
            file_path = export_specialties(format=format, filename=filename)
        elif data_type == 'references':
            file_path = export_references(format=format, filename=filename)
        elif data_type == 'guidelines':
            file_path = export_guidelines(format=format, filename=filename)
        else:  # 'all'
            file_path = export_all(format=format, filename=filename)
        
        # Log export
        logger.info(f"Data export: {data_type} in {format} format by user {current_user.username if current_user.is_authenticated else 'anonymous'}")
        
        return send_file(file_path, as_attachment=True)
    except Exception as e:
        logger.error(f"Export error: {str(e)}")
        flash(f"Export failed: {str(e)}", 'error')
        return redirect(url_for('export'))

@app.route('/about')
def about():
    """About page"""
    return render_template('about.html')

@app.route('/favorites/add/<string:item_type>/<int:item_id>', methods=['POST'])
@login_required
def add_favorite(item_type, item_id):
    """Add an item to user's favorites"""
    from models import Favorite
    
    # Check if already in favorites
    existing = Favorite.query.filter_by(
        user_id=current_user.id,
        item_type=item_type,
        item_id=item_id
    ).first()
    
    if existing:
        flash('Item already in favorites', 'info')
    else:
        # Add to favorites
        favorite = Favorite(
            user_id=current_user.id,
            item_type=item_type,
            item_id=item_id
        )
        db.session.add(favorite)
        db.session.commit()
        flash('Added to favorites', 'success')
    
    # Redirect back to the item page
    if item_type == 'condition':
        return redirect(url_for('condition_detail', condition_id=item_id))
    elif item_type == 'medication':
        return redirect(url_for('medication_detail', medication_id=item_id))
    elif item_type == 'reference':
        return redirect(url_for('reference_detail', reference_id=item_id))
    elif item_type == 'guideline':
        return redirect(url_for('guideline_detail', guideline_id=item_id))
    else:
        return redirect(url_for('index'))

@app.route('/favorites/remove/<string:item_type>/<int:item_id>', methods=['POST'])
@login_required
def remove_favorite(item_type, item_id):
    """Remove an item from user's favorites"""
    from models import Favorite
    
    favorite = Favorite.query.filter_by(
        user_id=current_user.id,
        item_type=item_type,
        item_id=item_id
    ).first()
    
    if favorite:
        db.session.delete(favorite)
        db.session.commit()
        flash('Removed from favorites', 'success')
    
    # Redirect back to profile or item page
    referrer = request.referrer
    if referrer and 'profile' in referrer:
        return redirect(url_for('auth.profile'))
    
    # Redirect to the appropriate item page
    if item_type == 'condition':
        return redirect(url_for('condition_detail', condition_id=item_id))
    elif item_type == 'medication':
        return redirect(url_for('medication_detail', medication_id=item_id))
    elif item_type == 'reference':
        return redirect(url_for('reference_detail', reference_id=item_id))
    elif item_type == 'guideline':
        return redirect(url_for('guideline_detail', guideline_id=item_id))
    else:
        return redirect(url_for('index'))

@app.route('/test')
def test_page():
    """Simple test page to verify the application is working"""
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Medical Reference App - Test Page</title>
        <style>
            body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
            h1 { color: #2c3e50; }
            ul { list-style-type: none; padding: 0; }
            li { margin-bottom: 10px; }
            a { color: #3498db; text-decoration: none; }
            a:hover { text-decoration: underline; }
            .specialty { font-weight: bold; margin-top: 20px; color: #2c3e50; }
        </style>
    </head>
    <body>
        <h1>Medical Reference App - Test Page</h1>
        <p>This is a test page to verify that the Flask application is working correctly.</p>
        
        <div class="specialty">Cardiology Medications</div>
        <ul>
            <li><a href="/medication/Lisinopril">Lisinopril</a></li>
            <li><a href="/medication/Atorvastatin">Atorvastatin</a></li>
        </ul>
        
        <div class="specialty">Neurology Medications</div>
        <ul>
            <li><a href="/medication/Levetiracetam">Levetiracetam</a></li>
        </ul>
        
        <div class="specialty">Dermatology Medications</div>
        <ul>
            <li><a href="/medication/Isotretinoin">Isotretinoin</a></li>
        </ul>
    </body>
    </html>
    """
    return html

@app.errorhandler(404)
def page_not_found(e):
    """Handle 404 errors"""
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(e):
    """Handle 500 errors"""
    logger.error(f"Server error: {str(e)}")
    return render_template('500.html'), 500

def generate_medication_relationships():
    """Generate relationships between medications based on class and specialty"""
    from models import Medication, MedicationRelationship, db
    
    # Clear existing relationships
    MedicationRelationship.query.delete()
    
    # Get all medications
    medications = Medication.query.all()
    
    # Dictionary to track processed pairs to avoid duplicates
    processed_pairs = set()
    
    # Create relationships based on same class
    for med1 in medications:
        for med2 in medications:
            # Skip self-relationships and already processed pairs
            if med1.id == med2.id or (med1.id, med2.id) in processed_pairs or (med2.id, med1.id) in processed_pairs:
                continue
                
            # Create relationship if medications are in the same class
            if med1.class_name and med2.class_name and med1.class_name == med2.class_name:
                relationship = MedicationRelationship(
                    medication_id=med1.id,
                    related_medication_id=med2.id,
                    relationship_type='same_class'
                )
                db.session.add(relationship)
                processed_pairs.add((med1.id, med2.id))
    
    # Create relationships based on similar uses
    for med1 in medications:
        for med2 in medications:
            # Skip self-relationships and already processed pairs
            if med1.id == med2.id or (med1.id, med2.id) in processed_pairs or (med2.id, med1.id) in processed_pairs:
                continue
                
            # Parse uses JSON
            uses1 = json.loads(med1.uses) if med1.uses else []
            uses2 = json.loads(med2.uses) if med2.uses else []
            
            # Check if medications have at least one common use
            common_uses = set(uses1) & set(uses2)
            if common_uses:
                relationship = MedicationRelationship(
                    medication_id=med1.id,
                    related_medication_id=med2.id,
                    relationship_type='similar_uses'
                )
                db.session.add(relationship)
                processed_pairs.add((med1.id, med2.id))
    
    # Commit changes
    db.session.commit()
    return f"Generated {len(processed_pairs)} medication relationships"

@app.route('/admin/generate-relationships')
@login_required
def admin_generate_relationships():
    """Admin route to generate medication relationships"""
    result = generate_medication_relationships()
    flash(result, 'success')
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        # Create database tables if they don't exist
        db.create_all()
        
        # Check if we need to create an admin user
        if User.query.filter_by(is_admin=True).first() is None:
            admin_user = User(
                username='admin',
                email='admin@example.com',
                is_admin=True
            )
            admin_user.set_password('admin')  # Set a default password
            db.session.add(admin_user)
            db.session.commit()
            print("Created admin user with username 'admin' and password 'admin'")
        
        # Generate medication relationships if they don't exist
        if MedicationRelationship.query.count() == 0:
            try:
                print("Generating medication relationships...")
                result = generate_medication_relationships()
                print(result)
            except Exception as e:
                print(f"Error generating medication relationships: {str(e)}")
    
    # Get port from environment variable or use default
    port = int(os.environ.get('PORT', 5000))
    
    # Start the Flask application
    app.run(host='0.0.0.0', port=port, debug=False)
