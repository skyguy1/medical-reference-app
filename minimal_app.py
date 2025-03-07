"""
Full-featured Medical Reference App with fallback mechanisms
"""
from flask import Flask, render_template, request, jsonify, send_file, url_for, redirect, flash
import json
import os
import logging
import traceback
from datetime import datetime
from flask_login import LoginManager, login_required, current_user

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

# Create Flask app
app = Flask(__name__)

# Get database URL from environment variable or use SQLite as fallback
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///medical_reference.db')
# Fix for Render's PostgreSQL URL format
if app.config['SQLALCHEMY_DATABASE_URI'] and app.config['SQLALCHEMY_DATABASE_URI'].startswith("postgres://"):
    app.config['SQLALCHEMY_DATABASE_URI'] = app.config['SQLALCHEMY_DATABASE_URI'].replace("postgres://", "postgresql://", 1)
    
logger.info(f"Using database: {app.config['SQLALCHEMY_DATABASE_URI']}")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')

# Import database models with fallback
try:
    from models import db, Condition, Medication, Specialty, Reference, Guideline, User, MedicationRelationship
    from flask_migrate import Migrate
    from utils import safe_json_loads
    import auth
    from auth import login_manager
    from api import api
    from cache import cache_result, clear_expired_cache
    
    # Initialize database
    db.init_app(app)
    migrate = Migrate(app, db)
    
    # Initialize login manager
    login_manager.init_app(app)
    
    # Register API blueprint
    app.register_blueprint(api, url_prefix='/api')
    
    MODELS_AVAILABLE = True
    logger.info("Database models loaded successfully")
except ImportError as e:
    logger.error(f"Error importing database models: {e}")
    logger.error(traceback.format_exc())
    MODELS_AVAILABLE = False

# Try to import visualization and export modules with fallback
try:
    from visualizations import (
        get_specialty_distribution, 
        get_medication_class_distribution,
        get_condition_network,
        get_reference_timeline,
        get_guideline_organization_distribution,
        get_condition_symptom_heatmap
    )
    VISUALIZATIONS_AVAILABLE = True
    logger.info("Visualization modules loaded successfully")
except ImportError as e:
    logger.error(f"Error importing visualization modules: {e}")
    logger.error(traceback.format_exc())
    VISUALIZATIONS_AVAILABLE = False

try:
    from export import (
        export_conditions,
        export_medications,
        export_specialties,
        export_references,
        export_guidelines,
        export_all
    )
    EXPORTS_AVAILABLE = True
    logger.info("Export modules loaded successfully")
except ImportError as e:
    logger.error(f"Error importing export modules: {e}")
    logger.error(traceback.format_exc())
    EXPORTS_AVAILABLE = False

# Routes
@app.route('/')
def index():
    """Home page"""
    if not MODELS_AVAILABLE:
        return """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Medical Reference App</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    max-width: 800px;
                    margin: 0 auto;
                    padding: 20px;
                    line-height: 1.6;
                }
                h1 {
                    color: #2c3e50;
                    border-bottom: 1px solid #eee;
                    padding-bottom: 10px;
                }
                .success {
                    color: green;
                    font-weight: bold;
                }
                .warning {
                    color: orange;
                    font-weight: bold;
                }
            </style>
        </head>
        <body>
            <h1>Medical Reference App</h1>
            <p class="success">✅ Deployment successful!</p>
            <p class="warning">⚠️ Running in limited functionality mode</p>
            <p>The application is running in a limited mode without database functionality.</p>
            <p>Please check the logs for more information.</p>
        </body>
        </html>
        """
    
    try:
        # Get counts for overview
        condition_count = Condition.query.count()
        medication_count = Medication.query.count()
        specialty_count = Specialty.query.count()
        reference_count = Reference.query.count()
        guideline_count = Guideline.query.count()
        
        return render_template('index.html', 
                            condition_count=condition_count,
                            medication_count=medication_count,
                            specialty_count=specialty_count,
                            reference_count=reference_count,
                            guideline_count=guideline_count)
    except Exception as e:
        logger.error(f"Error in index route: {e}")
        logger.error(traceback.format_exc())
        return """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Medical Reference App</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    max-width: 800px;
                    margin: 0 auto;
                    padding: 20px;
                    line-height: 1.6;
                }
                h1 {
                    color: #2c3e50;
                    border-bottom: 1px solid #eee;
                    padding-bottom: 10px;
                }
                .success {
                    color: green;
                    font-weight: bold;
                }
                .error {
                    color: red;
                    font-weight: bold;
                }
            </style>
        </head>
        <body>
            <h1>Medical Reference App</h1>
            <p class="success">✅ Deployment successful!</p>
            <p class="error">❌ Error loading data</p>
            <p>There was an error loading data from the database.</p>
            <p>Please check the logs for more information.</p>
        </body>
        </html>
        """

# Health check endpoint for Render
@app.route('/health')
def health():
    """Health check endpoint for Render"""
    status = {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "features": {
            "database": MODELS_AVAILABLE,
            "visualizations": VISUALIZATIONS_AVAILABLE,
            "exports": EXPORTS_AVAILABLE
        }
    }
    return jsonify(status)

# Include all other routes from the main app if models are available
if MODELS_AVAILABLE:
    # Condition routes
    @app.route('/conditions')
    @login_required
    def condition_list():
        """List all conditions"""
        conditions = Condition.query.order_by(Condition.name).all()
        return render_template('condition_list.html', conditions=conditions)
    
    @app.route('/conditions/<int:id>')
    @login_required
    def condition_detail(id):
        """Show condition details"""
        condition = Condition.query.get_or_404(id)
        return render_template('condition_detail.html', condition=condition)
    
    # Medication routes
    @app.route('/medications')
    @login_required
    def medication_list():
        """List all medications"""
        medications = Medication.query.order_by(Medication.name).all()
        return render_template('medication_list.html', medications=medications)
    
    @app.route('/medications/<int:id>')
    @login_required
    def medication_detail(id):
        """Show medication details"""
        medication = Medication.query.get_or_404(id)
        return render_template('medication_detail.html', medication=medication)
    
    # Specialty routes
    @app.route('/specialties')
    @login_required
    def specialty_list():
        """List all specialties"""
        specialties = Specialty.query.order_by(Specialty.name).all()
        return render_template('specialty_list.html', specialties=specialties)
    
    @app.route('/specialties/<int:id>')
    @login_required
    def specialty_detail(id):
        """Show specialty details"""
        specialty = Specialty.query.get_or_404(id)
        return render_template('specialty_detail.html', specialty=specialty)
    
    # Reference routes
    @app.route('/references')
    @login_required
    def reference_list():
        """List all references"""
        references = Reference.query.order_by(Reference.title).all()
        return render_template('reference_list.html', references=references)
    
    @app.route('/references/<int:id>')
    @login_required
    def reference_detail(id):
        """Show reference details"""
        reference = Reference.query.get_or_404(id)
        return render_template('reference_detail.html', reference=reference)
    
    # Guideline routes
    @app.route('/guidelines')
    @login_required
    def guideline_list():
        """List all guidelines"""
        guidelines = Guideline.query.order_by(Guideline.title).all()
        return render_template('guideline_list.html', guidelines=guidelines)
    
    @app.route('/guidelines/<int:id>')
    @login_required
    def guideline_detail(id):
        """Show guideline details"""
        guideline = Guideline.query.get_or_404(id)
        return render_template('guideline_detail.html', guideline=guideline)
    
    # Search route
    @app.route('/search')
    @login_required
    @cache_result(timeout=300)
    def search():
        """Search for medical information"""
        query = request.args.get('q', '')
        if not query:
            return render_template('search.html', results=None, query=None)
        
        # Search in conditions
        conditions = Condition.query.filter(
            Condition.name.ilike(f'%{query}%') | 
            Condition.description.ilike(f'%{query}%') |
            Condition.symptoms.ilike(f'%{query}%')
        ).all()
        
        # Search in medications
        medications = Medication.query.filter(
            Medication.name.ilike(f'%{query}%') | 
            Medication.description.ilike(f'%{query}%') |
            Medication.side_effects.ilike(f'%{query}%')
        ).all()
        
        # Search in specialties
        specialties = Specialty.query.filter(
            Specialty.name.ilike(f'%{query}%') | 
            Specialty.description.ilike(f'%{query}%')
        ).all()
        
        # Search in references
        references = Reference.query.filter(
            Reference.title.ilike(f'%{query}%') | 
            Reference.authors.ilike(f'%{query}%') |
            Reference.abstract.ilike(f'%{query}%')
        ).all()
        
        # Search in guidelines
        guidelines = Guideline.query.filter(
            Guideline.title.ilike(f'%{query}%') | 
            Guideline.organization.ilike(f'%{query}%') |
            Guideline.summary.ilike(f'%{query}%')
        ).all()
        
        results = {
            'conditions': conditions,
            'medications': medications,
            'specialties': specialties,
            'references': references,
            'guidelines': guidelines
        }
        
        return render_template('search.html', results=results, query=query)
    
    # Visualization routes
    @app.route('/visualizations')
    @login_required
    def visualizations():
        """Display data visualizations"""
        if not VISUALIZATIONS_AVAILABLE:
            flash('Visualizations are currently unavailable', 'error')
            return redirect(url_for('index'))
        
        # Get counts for overview
        condition_count = Condition.query.count()
        medication_count = Medication.query.count()
        specialty_count = Specialty.query.count()
        reference_count = Reference.query.count()
        guideline_count = Guideline.query.count()
        
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
                            guideline_count=guideline_count,
                            specialty_distribution=specialty_distribution,
                            medication_class_distribution=medication_class_distribution,
                            condition_network=condition_network,
                            reference_timeline=reference_timeline,
                            guideline_organization_distribution=guideline_organization_distribution,
                            condition_symptom_heatmap=condition_symptom_heatmap)
    
    # Export routes
    @app.route('/export')
    @login_required
    def export():
        """Export data page"""
        if not EXPORTS_AVAILABLE:
            flash('Exports are currently unavailable', 'error')
            return redirect(url_for('index'))
        
        return render_template('export.html')
    
    @app.route('/export/download')
    @login_required
    def export_download():
        """Download exported data"""
        if not EXPORTS_AVAILABLE:
            flash('Exports are currently unavailable', 'error')
            return redirect(url_for('index'))
        
        data_type = request.args.get('type', 'all')
        format = request.args.get('format', 'json')
        
        # Map data type to export function
        export_functions = {
            'conditions': export_conditions,
            'medications': export_medications,
            'specialties': export_specialties,
            'references': export_references,
            'guidelines': export_guidelines,
            'all': export_all
        }
        
        if data_type not in export_functions:
            flash(f'Invalid data type: {data_type}', 'error')
            return redirect(url_for('export'))
        
        try:
            # Call the appropriate export function
            filepath = export_functions[data_type](format)
            
            # Get filename from filepath
            filename = os.path.basename(filepath)
            
            # Send the file to the user
            return send_file(filepath, as_attachment=True, download_name=filename)
        except Exception as e:
            flash(f'Error exporting data: {str(e)}', 'error')
            return redirect(url_for('export'))
    
    # Authentication routes
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        """Login page"""
        if current_user.is_authenticated:
            return redirect(url_for('index'))
        
        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')
            
            user = User.query.filter_by(username=username).first()
            
            if user and user.check_password(password):
                auth.login_user(user)
                next_page = request.args.get('next')
                return redirect(next_page or url_for('index'))
            else:
                flash('Invalid username or password', 'error')
        
        return render_template('login.html')
    
    @app.route('/logout')
    @login_required
    def logout():
        """Logout user"""
        auth.logout_user()
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
