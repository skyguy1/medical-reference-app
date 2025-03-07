"""
Isolated Medical Reference App for Render deployment
"""
from flask import Flask, jsonify, render_template_string
import os
import logging
from datetime import datetime

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

# Basic HTML template
BASE_TEMPLATE = """
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
        h1, h2 {
            color: #2c3e50;
            border-bottom: 1px solid #eee;
            padding-bottom: 10px;
        }
        .success {
            color: green;
            font-weight: bold;
        }
        .info {
            color: blue;
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
    </style>
</head>
<body>
    <h1>Medical Reference App</h1>
    {{ content | safe }}
</body>
</html>
"""

# Routes
@app.route('/')
def index():
    """Home page"""
    content = """
    <p class="success">✅ Deployment successful!</p>
    <p>Welcome to the Medical Reference Application. This is a simplified version that has been successfully deployed to Render.</p>
    
    <h2>Available Features</h2>
    <div class="card">
        <h3>Health Check</h3>
        <p>The application provides a health check endpoint at <code>/health</code>.</p>
        <a href="/health-details" class="button">View Health Details</a>
    </div>
    
    <div class="card">
        <h3>System Information</h3>
        <p>View information about the current system environment.</p>
        <a href="/system-info" class="button">View System Info</a>
    </div>
    
    <h2>Next Steps</h2>
    <p>Now that we have a stable deployment, we can gradually add more features from the full application.</p>
    """
    return render_template_string(BASE_TEMPLATE, content=content)

@app.route('/health')
def health():
    """Health check endpoint for Render"""
    return jsonify({"status": "healthy"})

@app.route('/health-details')
def health_details():
    """Detailed health check information"""
    content = """
    <p class="info">Health Check Details</p>
    <div class="card">
        <h3>Status: <span class="success">Healthy</span></h3>
        <p>Last checked: {}</p>
        <p>Server time: {}</p>
        <p>Environment: {}</p>
    </div>
    <a href="/" class="button">Back to Home</a>
    """.format(
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        os.environ.get('FLASK_ENV', 'development')
    )
    return render_template_string(BASE_TEMPLATE, content=content)

@app.route('/system-info')
def system_info():
    """System information page"""
    content = """
    <p class="info">System Information</p>
    <div class="card">
        <h3>Environment Variables</h3>
        <ul>
            <li>FLASK_ENV: {}</li>
            <li>PYTHON_VERSION: {}</li>
        </ul>
    </div>
    <a href="/" class="button">Back to Home</a>
    """.format(
        os.environ.get('FLASK_ENV', 'Not set'),
        os.environ.get('PYTHON_VERSION', 'Not set')
    )
    return render_template_string(BASE_TEMPLATE, content=content)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
