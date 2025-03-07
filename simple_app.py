"""
Simplified version of the medical reference app for initial deployment testing
"""
from flask import Flask, render_template, jsonify
import os
import logging

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
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')

@app.route('/')
def index():
    """Simple index page for testing deployment"""
    return render_template('index.html')

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({"status": "ok"})

@app.route('/test')
def test():
    """Test page"""
    return """
    <html>
        <head>
            <title>Medical Reference App - Test Page</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 40px; line-height: 1.6; }
                h1 { color: #2c3e50; }
                .success { color: green; font-weight: bold; }
            </style>
        </head>
        <body>
            <h1>Medical Reference App</h1>
            <p class="success">✅ Deployment successful!</p>
            <p>This is a simplified test page to verify that the application is running correctly on Render.</p>
            <p>Environment: {}</p>
        </body>
    </html>
    """.format(os.environ.get('FLASK_ENV', 'development'))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
