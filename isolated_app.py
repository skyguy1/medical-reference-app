"""
Completely isolated Flask application for testing Render deployment
This file has no dependencies on any other files in the project
"""
from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
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
        </style>
    </head>
    <body>
        <h1>Medical Reference App</h1>
        <p class="success">✅ Deployment successful!</p>
        <p>This isolated application confirms that your Flask app is running correctly on Render.</p>
        <p>Once this works, we can gradually add more functionality.</p>
    </body>
    </html>
    """

@app.route('/health')
def health():
    return '{"status": "ok"}'

# This is the only entry point for the application
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
else:
    # This ensures the app is properly initialized when run by Gunicorn
    # without triggering imports from other modules
    pass
