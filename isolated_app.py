"""
Bridge application that properly imports and uses the standalone app
"""
import os
import sys
import importlib.util
from flask import Flask, request, jsonify, redirect

# Create a simple Flask app that will act as a bridge
app = Flask(__name__)

# Dynamically import the standalone app
standalone_app = None

def load_standalone_app():
    global standalone_app
    try:
        # Add the project root to the Python path
        root_dir = os.path.dirname(os.path.abspath(__file__))
        sys.path.insert(0, root_dir)
        
        # First, try to import directly
        try:
            from standalone.app import app as sa
            return sa
        except ImportError as e:
            print(f"Direct import failed: {e}")
        
        # If direct import fails, try spec-based import
        spec = importlib.util.spec_from_file_location(
            "standalone.app", 
            os.path.join(root_dir, "standalone", "app.py")
        )
        if spec:
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            return module.app
        else:
            raise ImportError("Could not find standalone app module")
    except Exception as e:
        print(f"Error loading standalone app: {str(e)}")
        return None

# Try to load the standalone app at startup
standalone_app = load_standalone_app()

@app.route('/')
def index():
    """Root route that either redirects to the standalone app or shows a fallback page"""
    if standalone_app:
        try:
            # Try to use the standalone app's index function
            return standalone_app.view_functions['index']()
        except Exception as e:
            print(f"Error using standalone index: {str(e)}")
    
    # Fallback to a simple page with diagnostic info
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Medical Reference App - Bridge</title>
        <style>
            body {{ font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; line-height: 1.6; }}
            h1 {{ color: #2c3e50; border-bottom: 1px solid #eee; padding-bottom: 10px; }}
            .message {{ color: blue; font-weight: bold; }}
            pre {{ background: #f5f5f5; padding: 10px; overflow: auto; }}
        </style>
    </head>
    <body>
        <h1>Medical Reference App</h1>
        <p class="message">Bridge Application</p>
        <p>Status: {'Connected to standalone app' if standalone_app else 'Standalone app not loaded'}</p>
        <p>Try accessing these routes:</p>
        <ul>
            <li><a href="/medications">/medications</a></li>
            <li><a href="/conditions">/conditions</a></li>
            <li><a href="/login">/login</a></li>
        </ul>
        <p>Python path:</p>
        <pre>{str(sys.path)}</pre>
        <p>Available modules:</p>
        <pre>{str(sys.modules.keys())}</pre>
    </body>
    </html>
    """

@app.route('/<path:subpath>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def proxy(subpath):
    """Proxy all other routes to the standalone app"""
    if not standalone_app:
        return jsonify({"error": "Standalone app not loaded"}), 500
    
    try:
        # Get the endpoint function from the standalone app
        endpoint = subpath
        if endpoint.endswith('/'):
            endpoint = endpoint[:-1]
        
        # Try to find the view function
        view_func = standalone_app.view_functions.get(endpoint)
        if view_func:
            return view_func()
        
        # If we couldn't find a direct match, try to find a route that matches
        for rule in standalone_app.url_map.iter_rules():
            if rule.endpoint != 'static' and subpath in rule.rule:
                view_func = standalone_app.view_functions.get(rule.endpoint)
                if view_func:
                    return view_func()
        
        # If we still couldn't find a match, return a 404
        return jsonify({"error": f"Route /{subpath} not found"}), 404
    except Exception as e:
        return jsonify({"error": f"Error processing request: {str(e)}"}), 500

@app.route('/health')
def health():
    """Health check endpoint for Render"""
    return jsonify({"status": "healthy", "standalone_loaded": standalone_app is not None})

# This is the only entry point for the application
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
