"""
Minimal Flask application for Render deployment
"""
from flask import Flask, jsonify, render_template_string
import os
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create Flask app
app = Flask(__name__)

# Basic HTML template
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Medical Reference App - Minimal</title>
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
    </style>
</head>
<body>
    <h1>Medical Reference App</h1>
    <div class="card">
        <p class="success">✅ Minimal deployment successful!</p>
        <p>This is a minimal version of the Medical Reference Application deployed on Render.</p>
        <p>Current time: {{ current_time }}</p>
        <p>Environment: {{ environment }}</p>
        <a href="/health" class="button">Health Check</a>
    </div>
</body>
</html>
"""

@app.route('/')
def index():
    """Home page"""
    try:
        return render_template_string(
            HTML_TEMPLATE,
            current_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            environment=os.environ.get('FLASK_ENV', 'development')
        )
    except Exception as e:
        logger.error(f"Error rendering index: {e}")
        return "Medical Reference App is running, but encountered an error rendering the template."

@app.route('/health')
def health():
    """Health check endpoint for Render"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "standalone-1.0"
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
