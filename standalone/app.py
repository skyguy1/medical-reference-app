"""
Medical Reference App with database models and authentication
"""
from flask import Flask, jsonify, render_template_string, request, redirect, url_for, flash, send_file, session
import os
import logging
import json
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///medical_reference.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Import and initialize database models
try:
    from models import db, User, Condition, Medication, Specialty, Reference, Guideline
    from auth import auth_bp, login_manager, create_admin_user
    
    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    
    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix='/auth')
    
    # Initialize database and create admin user
    with app.app_context():
        db.create_all()
        create_admin_user(app)
    
    models_available = True
    logger.info("Database models and authentication initialized successfully")
except ImportError as e:
    logger.error(f"Error importing models or auth: {e}")
    models_available = False

# Ensure the instance folder exists
os.makedirs(app.instance_path, exist_ok=True)

# Create export directory
EXPORT_DIR = os.path.join(app.instance_path, 'exports')
os.makedirs(EXPORT_DIR, exist_ok=True)

# Basic HTML template
BASE_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Medical Reference App</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            line-height: 1.6;
        }
        h1, h2, h3 {
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
        .error {
            color: red;
            font-weight: bold;
        }
        .card {
            border: 1px solid #ddd;
            border-radius: 4px;
            padding: 15px;
            margin-bottom: 15px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .button {
            display: inline-block;
            background-color: #3498db;
            color: white;
            padding: 8px 16px;
            text-decoration: none;
            border-radius: 4px;
            margin-top: 10px;
        }
        .button:hover {
            background-color: #2980b9;
        }
        .container {
            display: flex;
            flex-wrap: wrap;
        }
        .sidebar {
            flex: 1;
            min-width: 200px;
            padding-right: 20px;
        }
        .content {
            flex: 3;
            min-width: 300px;
        }
        table {
            width: 100%;
            border-collapse: collapse;
        }
        table, th, td {
            border: 1px solid #ddd;
        }
        th, td {
            padding: 8px;
            text-align: left;
        }
        th {
            background-color: #f2f2f2;
        }
        tr:nth-child(even) {
            background-color: #f9f9f9;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="sidebar">
            <h2>Navigation</h2>
            <ul>
                <li><a href="/">Home</a></li>
                {% if models_available %}
                <li><a href="/conditions">Conditions</a></li>
                <li><a href="/medications">Medications</a></li>
                <li><a href="/specialties">Specialties</a></li>
                <li><a href="/references">References</a></li>
                <li><a href="/guidelines">Guidelines</a></li>
                <li><a href="/search">Search</a></li>
                {% endif %}
                <li><a href="/health">Health Check</a></li>
                <li><a href="/system-info">System Info</a></li>
            </ul>
            
            {% if models_available %}
            <h2>Export Data</h2>
            <ul>
                <li><a href="/export/conditions">Export Conditions</a></li>
                <li><a href="/export/medications">Export Medications</a></li>
                <li><a href="/export/specialties">Export Specialties</a></li>
                <li><a href="/export/references">Export References</a></li>
                <li><a href="/export/guidelines">Export Guidelines</a></li>
            </ul>
            {% endif %}
        </div>
        
        <div class="content">
            <h1>Medical Reference App</h1>
            {{ content | safe }}
        </div>
    </div>
</body>
</html>
"""

# Store base template in session for auth module
session['base_template'] = BASE_TEMPLATE

# Routes
@app.route('/')
def index():
    """Home page"""
    if not models_available:
        content = """
        <div class="card">
            <p class="success">✅ Deployment successful!</p>
            <p>This is a minimal version of the Medical Reference Application deployed on Render.</p>
            <p class="warning">⚠️ Database models are not available. Only basic functionality is enabled.</p>
            <p>Current time: {}</p>
            <p>Environment: {}</p>
        </div>
        """.format(
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            os.environ.get('FLASK_ENV', 'development')
        )
    else:
        try:
            stats = {
                'conditions': Condition.query.count(),
                'medications': Medication.query.count(),
                'specialties': Specialty.query.count(),
                'references': Reference.query.count(),
                'guidelines': Guideline.query.count()
            }
            
            content = """
            <div class="card">
                <p class="success">✅ Deployment successful with database models!</p>
                <p>Welcome to the Medical Reference Application. This version includes database functionality.</p>
                <p>Current time: {}</p>
                <p>Environment: {}</p>
            </div>
            
            <h2>Database Statistics</h2>
            <div class="card">
                <table>
                    <tr>
                        <th>Entity</th>
                        <th>Count</th>
                        <th>Action</th>
                    </tr>
                    <tr>
                        <td>Conditions</td>
                        <td>{}</td>
                        <td><a href="/conditions" class="button">View</a></td>
                    </tr>
                    <tr>
                        <td>Medications</td>
                        <td>{}</td>
                        <td><a href="/medications" class="button">View</a></td>
                    </tr>
                    <tr>
                        <td>Specialties</td>
                        <td>{}</td>
                        <td><a href="/specialties" class="button">View</a></td>
                    </tr>
                    <tr>
                        <td>References</td>
                        <td>{}</td>
                        <td><a href="/references" class="button">View</a></td>
                    </tr>
                    <tr>
                        <td>Guidelines</td>
                        <td>{}</td>
                        <td><a href="/guidelines" class="button">View</a></td>
                    </tr>
                </table>
            </div>
            """.format(
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                os.environ.get('FLASK_ENV', 'development'),
                stats['conditions'],
                stats['medications'],
                stats['specialties'],
                stats['references'],
                stats['guidelines']
            )
        except Exception as e:
            logger.error(f"Error loading database statistics: {e}")
            content = """
            <div class="card">
                <p class="success">✅ Deployment successful!</p>
                <p class="warning">⚠️ Database is configured but an error occurred: {}</p>
                <p>Current time: {}</p>
                <p>Environment: {}</p>
            </div>
            """.format(
                str(e),
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                os.environ.get('FLASK_ENV', 'development')
            )
    
    return render_template_string(
        BASE_TEMPLATE,
        content=content,
        models_available=models_available
    )

@app.route('/conditions')
def condition_list():
    """List all conditions"""
    if not models_available:
        content = """
        <div class="card">
            <p class="error">❌ Database models are not available</p>
            <p>This feature requires database functionality.</p>
            <a href="/" class="button">Back to Home</a>
        </div>
        """
    else:
        try:
            conditions = Condition.query.all()
            
            conditions_html = ""
            for condition in conditions:
                conditions_html += f"""
                <tr>
                    <td>{condition.id}</td>
                    <td>{condition.name}</td>
                    <td>{condition.description[:100]}...</td>
                    <td><a href="/conditions/{condition.id}" class="button">View</a></td>
                </tr>
                """
            
            content = f"""
            <h2>Conditions</h2>
            <div class="card">
                <table>
                    <tr>
                        <th>ID</th>
                        <th>Name</th>
                        <th>Description</th>
                        <th>Action</th>
                    </tr>
                    {conditions_html if conditions else "<tr><td colspan='4'>No conditions found</td></tr>"}
                </table>
            </div>
            """
        except Exception as e:
            logger.error(f"Error loading conditions: {e}")
            content = f"""
            <div class="card">
                <p class="error">❌ Error loading conditions: {str(e)}</p>
                <a href="/" class="button">Back to Home</a>
            </div>
            """
    
    return render_template_string(
        BASE_TEMPLATE,
        content=content,
        models_available=models_available
    )

@app.route('/conditions/<int:id>')
def condition_detail(id):
    """Show condition details"""
    if not models_available:
        content = """
        <div class="card">
            <p class="error">❌ Database models are not available</p>
            <p>This feature requires database functionality.</p>
            <a href="/" class="button">Back to Home</a>
        </div>
        """
    else:
        try:
            condition = Condition.query.get_or_404(id)
            
            specialties_html = ""
            for specialty in condition.specialties:
                specialties_html += f"<li>{specialty.name}</li>"
            
            medications_html = ""
            for medication in condition.medications:
                medications_html += f"<li>{medication.name}</li>"
            
            content = f"""
            <h2>Condition: {condition.name}</h2>
            <div class="card">
                <h3>Details</h3>
                <table>
                    <tr>
                        <th>ID</th>
                        <td>{condition.id}</td>
                    </tr>
                    <tr>
                        <th>Name</th>
                        <td>{condition.name}</td>
                    </tr>
                    <tr>
                        <th>Description</th>
                        <td>{condition.description}</td>
                    </tr>
                    <tr>
                        <th>Symptoms</th>
                        <td>{condition.symptoms}</td>
                    </tr>
                    <tr>
                        <th>Created</th>
                        <td>{condition.created_at}</td>
                    </tr>
                    <tr>
                        <th>Updated</th>
                        <td>{condition.updated_at}</td>
                    </tr>
                </table>
                
                <h3>Specialties</h3>
                <ul>
                    {specialties_html if specialties_html else "<li>No specialties associated</li>"}
                </ul>
                
                <h3>Medications</h3>
                <ul>
                    {medications_html if medications_html else "<li>No medications associated</li>"}
                </ul>
                
                <a href="/conditions" class="button">Back to Conditions</a>
            </div>
            """
        except Exception as e:
            logger.error(f"Error loading condition {id}: {e}")
            content = f"""
            <div class="card">
                <p class="error">❌ Error loading condition: {str(e)}</p>
                <a href="/conditions" class="button">Back to Conditions</a>
            </div>
            """
    
    return render_template_string(
        BASE_TEMPLATE,
        content=content,
        models_available=models_available
    )

@app.route('/export/<entity_type>')
def export(entity_type):
    """Export data without pandas"""
    if not models_available:
        content = """
        <div class="card">
            <p class="error">❌ Database models are not available</p>
            <p>This feature requires database functionality.</p>
            <a href="/" class="button">Back to Home</a>
        </div>
        """
        return render_template_string(
            BASE_TEMPLATE,
            content=content,
            models_available=models_available
        )
    
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
            content = f"""
            <div class="card">
                <p class="error">❌ Invalid export type: {entity_type}</p>
                <a href="/" class="button">Back to Home</a>
            </div>
            """
            return render_template_string(
                BASE_TEMPLATE,
                content=content,
                models_available=models_available
            )
        
        # Export as JSON (no pandas dependency)
        filename = f"{entity_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        filepath = os.path.join(EXPORT_DIR, filename)
        
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2, default=str)
        
        return send_file(filepath, as_attachment=True, download_name=filename)
    except Exception as e:
        logger.error(f"Error during export: {e}")
        content = f"""
        <div class="card">
            <p class="error">❌ Error during export: {str(e)}</p>
            <a href="/" class="button">Back to Home</a>
        </div>
        """
        return render_template_string(
            BASE_TEMPLATE,
            content=content,
            models_available=models_available
        )

@app.route('/health')
def health():
    """Health check endpoint for Render"""
    status = {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "database": "available" if models_available else "unavailable",
        "version": "1.0.0"
    }
    return jsonify(status)

@app.route('/system-info')
def system_info():
    """System information page"""
    try:
        content = """
        <h2>System Information</h2>
        <div class="card">
            <h3>Environment</h3>
            <table>
                <tr>
                    <th>Flask Environment</th>
                    <td>{}</td>
                </tr>
                <tr>
                    <th>Python Version</th>
                    <td>{}</td>
                </tr>
                <tr>
                    <th>Server Time</th>
                    <td>{}</td>
                </tr>
            </table>
        </div>
        
        <div class="card">
            <h3>Database</h3>
            <table>
                <tr>
                    <th>Database URL</th>
                    <td>{}</td>
                </tr>
                <tr>
                    <th>Models Available</th>
                    <td>{}</td>
                </tr>
            </table>
        </div>
        """.format(
            os.environ.get('FLASK_ENV', 'development'),
            os.environ.get('PYTHON_VERSION', 'unknown'),
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            app.config['SQLALCHEMY_DATABASE_URI'],
            '<span class="success">Yes</span>' if models_available else '<span class="error">No</span>'
        )
    except Exception as e:
        logger.error(f"Error loading system info: {e}")
        content = f"""
        <div class="card">
            <p class="error">❌ Error loading system information: {str(e)}</p>
            <a href="/" class="button">Back to Home</a>
        </div>
        """
    
    return render_template_string(
        BASE_TEMPLATE,
        content=content,
        models_available=models_available
    )

@app.errorhandler(404)
def page_not_found(e):
    """Handle 404 errors"""
    content = """
    <div class="card">
        <h2>Page Not Found</h2>
        <p>The requested page does not exist.</p>
        <a href="/" class="button">Back to Home</a>
    </div>
    """
    return render_template_string(
        BASE_TEMPLATE,
        content=content,
        models_available=models_available
    ), 404

@app.errorhandler(500)
def server_error(e):
    """Handle 500 errors"""
    logger.error(f"Server error: {e}")
    content = """
    <div class="card">
        <h2>Server Error</h2>
        <p>An internal server error occurred.</p>
        <a href="/" class="button">Back to Home</a>
    </div>
    """
    return render_template_string(
        BASE_TEMPLATE,
        content=content,
        models_available=models_available
    ), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
