"""
Standalone Flask application for testing Render deployment
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
        <p>This standalone application confirms that your Flask app is running correctly on Render.</p>
        <p>Once this works, we can gradually add more functionality.</p>
    </body>
    </html>
    """

@app.route('/health')
def health():
    return '{"status": "ok"}'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
