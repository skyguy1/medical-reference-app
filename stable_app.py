"""
Stable Medical Reference App without pandas dependencies
"""
from flask import Flask, jsonify, render_template, request, redirect, url_for, flash, send_file
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
import os
import logging
import json
from datetime import datetime
from werkzeug.utils import secure_filename

# Import models
try:
    from simplified_models import db, User, Condition, Medication, Specialty, Reference, Guideline, MedicationRelationship
    models_available = True
except ImportError as e:
    logging.error(f"Error importing models: {e}")
    models_available = False

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Create Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///medical_reference.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
if models_available:
    db.init_app(app)
    
    # Initialize login manager
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'login'
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

# Ensure the instance folder exists
os.makedirs(app.instance_path, exist_ok=True)

# Create export directory
EXPORT_DIR = os.path.join(app.instance_path, 'exports')
os.makedirs(EXPORT_DIR, exist_ok=True)

# Routes
@app.route('/')
def index():
    """Home page"""
    if not models_available:
        return render_template('error.html', 
                              title="Database Not Available", 
                              message="The database models could not be loaded. Basic functionality is still available.")
    
    try:
        stats = {
            'conditions': Condition.query.count(),
            'medications': Medication.query.count(),
            'specialties': Specialty.query.count(),
            'references': Reference.query.count(),
            'guidelines': Guideline.query.count()
        }
        return render_template('index.html', stats=stats)
    except Exception as e:
        logger.error(f"Error loading index page: {e}")
        return render_template('error.html', 
                              title="Database Error", 
                              message="Could not load database statistics. Please try again later.")

@app.route('/conditions')
def condition_list():
    """List all conditions"""
    if not models_available:
        return render_template('error.html', 
                              title="Database Not Available", 
                              message="The database models could not be loaded.")
    
    try:
        conditions = Condition.query.all()
        return render_template('condition_list.html', conditions=conditions)
    except Exception as e:
        logger.error(f"Error loading conditions: {e}")
        return render_template('error.html', 
                              title="Database Error", 
                              message="Could not load conditions. Please try again later.")

@app.route('/conditions/<int:id>')
def condition_detail(id):
    """Show condition details"""
    if not models_available:
        return render_template('error.html', 
                              title="Database Not Available", 
                              message="The database models could not be loaded.")
    
    try:
        condition = Condition.query.get_or_404(id)
        return render_template('condition_detail.html', condition=condition)
    except Exception as e:
        logger.error(f"Error loading condition {id}: {e}")
        return render_template('error.html', 
                              title="Database Error", 
                              message=f"Could not load condition with ID {id}. Please try again later.")

@app.route('/medications')
def medication_list():
    """List all medications"""
    if not models_available:
        return render_template('error.html', 
                              title="Database Not Available", 
                              message="The database models could not be loaded.")
    
    try:
        medications = Medication.query.all()
        return render_template('medication_list.html', medications=medications)
    except Exception as e:
        logger.error(f"Error loading medications: {e}")
        return render_template('error.html', 
                              title="Database Error", 
                              message="Could not load medications. Please try again later.")

@app.route('/medications/<int:id>')
def medication_detail(id):
    """Show medication details"""
    if not models_available:
        return render_template('error.html', 
                              title="Database Not Available", 
                              message="The database models could not be loaded.")
    
    try:
        medication = Medication.query.get_or_404(id)
        return render_template('medication_detail.html', medication=medication)
    except Exception as e:
        logger.error(f"Error loading medication {id}: {e}")
        return render_template('error.html', 
                              title="Database Error", 
                              message=f"Could not load medication with ID {id}. Please try again later.")

@app.route('/specialties')
def specialty_list():
    """List all specialties"""
    if not models_available:
        return render_template('error.html', 
                              title="Database Not Available", 
                              message="The database models could not be loaded.")
    
    try:
        specialties = Specialty.query.all()
        return render_template('specialty_list.html', specialties=specialties)
    except Exception as e:
        logger.error(f"Error loading specialties: {e}")
        return render_template('error.html', 
                              title="Database Error", 
                              message="Could not load specialties. Please try again later.")

@app.route('/specialties/<int:id>')
def specialty_detail(id):
    """Show specialty details"""
    if not models_available:
        return render_template('error.html', 
                              title="Database Not Available", 
                              message="The database models could not be loaded.")
    
    try:
        specialty = Specialty.query.get_or_404(id)
        return render_template('specialty_detail.html', specialty=specialty)
    except Exception as e:
        logger.error(f"Error loading specialty {id}: {e}")
        return render_template('error.html', 
                              title="Database Error", 
                              message=f"Could not load specialty with ID {id}. Please try again later.")

@app.route('/references')
def reference_list():
    """List all references"""
    if not models_available:
        return render_template('error.html', 
                              title="Database Not Available", 
                              message="The database models could not be loaded.")
    
    try:
        references = Reference.query.all()
        return render_template('reference_list.html', references=references)
    except Exception as e:
        logger.error(f"Error loading references: {e}")
        return render_template('error.html', 
                              title="Database Error", 
                              message="Could not load references. Please try again later.")

@app.route('/references/<int:id>')
def reference_detail(id):
    """Show reference details"""
    if not models_available:
        return render_template('error.html', 
                              title="Database Not Available", 
                              message="The database models could not be loaded.")
    
    try:
        reference = Reference.query.get_or_404(id)
        return render_template('reference_detail.html', reference=reference)
    except Exception as e:
        logger.error(f"Error loading reference {id}: {e}")
        return render_template('error.html', 
                              title="Database Error", 
                              message=f"Could not load reference with ID {id}. Please try again later.")

@app.route('/guidelines')
def guideline_list():
    """List all guidelines"""
    if not models_available:
        return render_template('error.html', 
                              title="Database Not Available", 
                              message="The database models could not be loaded.")
    
    try:
        guidelines = Guideline.query.all()
        return render_template('guideline_list.html', guidelines=guidelines)
    except Exception as e:
        logger.error(f"Error loading guidelines: {e}")
        return render_template('error.html', 
                              title="Database Error", 
                              message="Could not load guidelines. Please try again later.")

@app.route('/guidelines/<int:id>')
def guideline_detail(id):
    """Show guideline details"""
    if not models_available:
        return render_template('error.html', 
                              title="Database Not Available", 
                              message="The database models could not be loaded.")
    
    try:
        guideline = Guideline.query.get_or_404(id)
        return render_template('guideline_detail.html', guideline=guideline)
    except Exception as e:
        logger.error(f"Error loading guideline {id}: {e}")
        return render_template('error.html', 
                              title="Database Error", 
                              message=f"Could not load guideline with ID {id}. Please try again later.")

@app.route('/search')
def search():
    """Search for medical information"""
    if not models_available:
        return render_template('error.html', 
                              title="Database Not Available", 
                              message="The database models could not be loaded. Search is not available.")
    
    query = request.args.get('q', '')
    if not query:
        return render_template('search.html', results=None)
    
    try:
        # Simple search implementation without pandas
        conditions = Condition.query.filter(Condition.name.ilike(f'%{query}%') | 
                                           Condition.description.ilike(f'%{query}%')).all()
        
        medications = Medication.query.filter(Medication.name.ilike(f'%{query}%') | 
                                             Medication.description.ilike(f'%{query}%')).all()
        
        specialties = Specialty.query.filter(Specialty.name.ilike(f'%{query}%') | 
                                            Specialty.description.ilike(f'%{query}%')).all()
        
        references = Reference.query.filter(Reference.title.ilike(f'%{query}%') | 
                                           Reference.abstract.ilike(f'%{query}%')).all()
        
        guidelines = Guideline.query.filter(Guideline.title.ilike(f'%{query}%') | 
                                           Guideline.summary.ilike(f'%{query}%')).all()
        
        results = {
            'conditions': conditions,
            'medications': medications,
            'specialties': specialties,
            'references': references,
            'guidelines': guidelines
        }
        
        return render_template('search.html', results=results, query=query)
    except Exception as e:
        logger.error(f"Error during search: {e}")
        return render_template('error.html', 
                              title="Search Error", 
                              message="An error occurred during search. Please try again later.")

@app.route('/export/<entity_type>')
def export(entity_type):
    """Export data without pandas"""
    if not models_available:
        return render_template('error.html', 
                              title="Database Not Available", 
                              message="The database models could not be loaded. Export is not available.")
    
    try:
        # Get data based on entity type
        data = []
        if entity_type == 'conditions':
            items = Condition.query.all()
            data = [item.to_dict() for item in items]
        elif entity_type == 'medications':
            items = Medication.query.all()
            data = [item.to_dict() for item in items]
        elif entity_type == 'specialties':
            items = Specialty.query.all()
            data = [item.to_dict() for item in items]
        elif entity_type == 'references':
            items = Reference.query.all()
            data = [item.to_dict() for item in items]
        elif entity_type == 'guidelines':
            items = Guideline.query.all()
            data = [item.to_dict() for item in items]
        else:
            return render_template('error.html', 
                                  title="Invalid Export Type", 
                                  message=f"Export type '{entity_type}' is not supported.")
        
        # Export as JSON (no pandas dependency)
        filename = f"{entity_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        filepath = os.path.join(EXPORT_DIR, filename)
        
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2, default=str)
        
        return send_file(filepath, as_attachment=True)
    except Exception as e:
        logger.error(f"Error during export: {e}")
        return render_template('error.html', 
                              title="Export Error", 
                              message=f"An error occurred during export: {str(e)}")

@app.route('/health')
def health():
    """Health check endpoint for Render"""
    status = {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "database": "available" if models_available else "unavailable"
    }
    return jsonify(status)

@app.route('/system-info')
def system_info():
    """System information page"""
    info = {
        "flask_env": os.environ.get('FLASK_ENV', 'development'),
        "python_version": os.environ.get('PYTHON_VERSION', 'unknown'),
        "database_url": app.config['SQLALCHEMY_DATABASE_URI'],
        "models_available": models_available,
        "server_time": datetime.now().isoformat()
    }
    return render_template('system_info.html', info=info)

@app.errorhandler(404)
def page_not_found(e):
    """Handle 404 errors"""
    return render_template('error.html', title="Page Not Found", message="The requested page does not exist."), 404

@app.errorhandler(500)
def server_error(e):
    """Handle 500 errors"""
    logger.error(f"Server error: {e}")
    return render_template('error.html', title="Server Error", message="An internal server error occurred."), 500

# Initialize database if available
def init_db():
    """Initialize the database"""
    if models_available:
        with app.app_context():
            db.create_all()
            logger.info("Database tables created.")

if __name__ == '__main__':
    # Initialize database
    init_db()
    
    # Run app
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
