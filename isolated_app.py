"""
Direct implementation of the Medical Reference App
This file directly implements the essential functionality without dependencies
"""
import os
import sys
from flask import Flask, jsonify, send_from_directory

# Create a simple Flask app
app = Flask(__name__)

@app.route('/')
def index():
    """Root route that shows a simple page with links to other routes"""
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Medical Reference App</title>
        <style>
            body {{ font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; line-height: 1.6; }}
            h1 {{ color: #2c3e50; border-bottom: 1px solid #eee; padding-bottom: 10px; }}
            .message {{ color: green; font-weight: bold; }}
            .card {{ border: 1px solid #ddd; border-radius: 8px; padding: 16px; margin-bottom: 16px; }}
            .card h2 {{ margin-top: 0; color: #3498db; }}
            .btn {{ display: inline-block; background-color: #3498db; color: white; padding: 8px 16px; 
                   text-decoration: none; border-radius: 4px; margin-right: 8px; }}
            .btn:hover {{ background-color: #2980b9; }}
        </style>
    </head>
    <body>
        <h1>Medical Reference App</h1>
        <p class="message">✅ Application is running successfully!</p>
        
        <div class="card">
            <h2>Medications</h2>
            <p>Browse our comprehensive database of medications, including dosage information, side effects, and contraindications.</p>
            <a href="/medications" class="btn">View Medications</a>
        </div>
        
        <div class="card">
            <h2>Conditions</h2>
            <p>Learn about various medical conditions, their symptoms, diagnosis methods, and treatment options.</p>
            <a href="/conditions" class="btn">View Conditions</a>
        </div>
        
        <div class="card">
            <h2>Specialties</h2>
            <p>Explore medical specialties and find related conditions, medications, and guidelines.</p>
            <a href="/specialties" class="btn">View Specialties</a>
        </div>
        
        <div class="card">
            <h2>Guidelines</h2>
            <p>Access evidence-based clinical guidelines from reputable medical organizations.</p>
            <a href="/guidelines" class="btn">View Guidelines</a>
        </div>
        
        <div class="card">
            <h2>User Account</h2>
            <p>Log in to access personalized features or create a new account.</p>
            <a href="/login" class="btn">Login</a>
            <a href="/register" class="btn">Register</a>
        </div>
    </body>
    </html>
    """

@app.route('/medications')
def medications():
    """Route that shows a list of medications"""
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Medications - Medical Reference App</title>
        <style>
            body {{ font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; line-height: 1.6; }}
            h1 {{ color: #2c3e50; border-bottom: 1px solid #eee; padding-bottom: 10px; }}
            .card {{ border: 1px solid #ddd; border-radius: 8px; padding: 16px; margin-bottom: 16px; }}
            .card h2 {{ margin-top: 0; color: #3498db; }}
            .btn {{ display: inline-block; background-color: #3498db; color: white; padding: 8px 16px; 
                   text-decoration: none; border-radius: 4px; }}
            .btn:hover {{ background-color: #2980b9; }}
            .home-link {{ margin-bottom: 20px; }}
        </style>
    </head>
    <body>
        <div class="home-link">
            <a href="/" class="btn">Home</a>
        </div>
        
        <h1>Medications</h1>
        
        <div class="card">
            <h2>Aspirin</h2>
            <p><strong>Generic Name:</strong> Acetylsalicylic acid</p>
            <p><strong>Drug Class:</strong> NSAID</p>
            <p><strong>Description:</strong> Common pain reliever and anti-inflammatory</p>
            <a href="/medications/1" class="btn">View Details</a>
        </div>
        
        <div class="card">
            <h2>Lisinopril</h2>
            <p><strong>Generic Name:</strong> Lisinopril</p>
            <p><strong>Drug Class:</strong> ACE Inhibitor</p>
            <p><strong>Description:</strong> Used to treat high blood pressure and heart failure</p>
            <a href="/medications/2" class="btn">View Details</a>
        </div>
        
        <div class="card">
            <h2>Prozac</h2>
            <p><strong>Generic Name:</strong> Fluoxetine</p>
            <p><strong>Drug Class:</strong> SSRI</p>
            <p><strong>Description:</strong> Antidepressant used to treat depression, OCD, and panic attacks</p>
            <a href="/medications/3" class="btn">View Details</a>
        </div>
    </body>
    </html>
    """

@app.route('/conditions')
def conditions():
    """Route that shows a list of conditions"""
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Conditions - Medical Reference App</title>
        <style>
            body {{ font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; line-height: 1.6; }}
            h1 {{ color: #2c3e50; border-bottom: 1px solid #eee; padding-bottom: 10px; }}
            .card {{ border: 1px solid #ddd; border-radius: 8px; padding: 16px; margin-bottom: 16px; }}
            .card h2 {{ margin-top: 0; color: #3498db; }}
            .btn {{ display: inline-block; background-color: #3498db; color: white; padding: 8px 16px; 
                   text-decoration: none; border-radius: 4px; }}
            .btn:hover {{ background-color: #2980b9; }}
            .home-link {{ margin-bottom: 20px; }}
        </style>
    </head>
    <body>
        <div class="home-link">
            <a href="/" class="btn">Home</a>
        </div>
        
        <h1>Medical Conditions</h1>
        
        <div class="card">
            <h2>Hypertension</h2>
            <p><strong>Description:</strong> High blood pressure</p>
            <p><strong>Symptoms:</strong> Usually asymptomatic, headache, shortness of breath</p>
            <a href="/conditions/1" class="btn">View Details</a>
        </div>
        
        <div class="card">
            <h2>Major Depressive Disorder</h2>
            <p><strong>Description:</strong> Mood disorder causing persistent feeling of sadness</p>
            <p><strong>Symptoms:</strong> Persistent sadness, loss of interest, sleep disturbances</p>
            <a href="/conditions/2" class="btn">View Details</a>
        </div>
        
        <div class="card">
            <h2>Migraine</h2>
            <p><strong>Description:</strong> Recurring headaches of moderate to severe intensity</p>
            <p><strong>Symptoms:</strong> Throbbing pain, nausea, sensitivity to light and sound</p>
            <a href="/conditions/3" class="btn">View Details</a>
        </div>
    </body>
    </html>
    """

@app.route('/specialties')
def specialties():
    """Route that shows a list of specialties"""
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Specialties - Medical Reference App</title>
        <style>
            body {{ font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; line-height: 1.6; }}
            h1 {{ color: #2c3e50; border-bottom: 1px solid #eee; padding-bottom: 10px; }}
            .card {{ border: 1px solid #ddd; border-radius: 8px; padding: 16px; margin-bottom: 16px; }}
            .card h2 {{ margin-top: 0; color: #3498db; }}
            .btn {{ display: inline-block; background-color: #3498db; color: white; padding: 8px 16px; 
                   text-decoration: none; border-radius: 4px; }}
            .btn:hover {{ background-color: #2980b9; }}
            .home-link {{ margin-bottom: 20px; }}
        </style>
    </head>
    <body>
        <div class="home-link">
            <a href="/" class="btn">Home</a>
        </div>
        
        <h1>Medical Specialties</h1>
        
        <div class="card">
            <h2>Cardiology</h2>
            <p><strong>Description:</strong> Deals with disorders of the heart and blood vessels</p>
            <a href="/specialties/1" class="btn">View Details</a>
        </div>
        
        <div class="card">
            <h2>Neurology</h2>
            <p><strong>Description:</strong> Focuses on disorders of the nervous system</p>
            <a href="/specialties/2" class="btn">View Details</a>
        </div>
        
        <div class="card">
            <h2>Pediatrics</h2>
            <p><strong>Description:</strong> Medical care of infants, children, and adolescents</p>
            <a href="/specialties/3" class="btn">View Details</a>
        </div>
        
        <div class="card">
            <h2>Psychiatry</h2>
            <p><strong>Description:</strong> Diagnosis, prevention, and treatment of mental disorders</p>
            <a href="/specialties/4" class="btn">View Details</a>
        </div>
    </body>
    </html>
    """

@app.route('/guidelines')
def guidelines():
    """Route that shows a list of guidelines"""
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Guidelines - Medical Reference App</title>
        <style>
            body {{ font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; line-height: 1.6; }}
            h1 {{ color: #2c3e50; border-bottom: 1px solid #eee; padding-bottom: 10px; }}
            .card {{ border: 1px solid #ddd; border-radius: 8px; padding: 16px; margin-bottom: 16px; }}
            .card h2 {{ margin-top: 0; color: #3498db; }}
            .btn {{ display: inline-block; background-color: #3498db; color: white; padding: 8px 16px; 
                   text-decoration: none; border-radius: 4px; }}
            .btn:hover {{ background-color: #2980b9; }}
            .home-link {{ margin-bottom: 20px; }}
        </style>
    </head>
    <body>
        <div class="home-link">
            <a href="/" class="btn">Home</a>
        </div>
        
        <h1>Clinical Guidelines</h1>
        
        <div class="card">
            <h2>Hypertension Management Guidelines</h2>
            <p><strong>Source:</strong> American Heart Association</p>
            <p><strong>Published:</strong> January 15, 2023</p>
            <p><strong>Summary:</strong> Guidelines for diagnosis and treatment of hypertension</p>
            <a href="/guidelines/1" class="btn">View Details</a>
        </div>
        
        <div class="card">
            <h2>Depression Treatment Guidelines</h2>
            <p><strong>Source:</strong> American Psychiatric Association</p>
            <p><strong>Published:</strong> June 10, 2022</p>
            <p><strong>Summary:</strong> Guidelines for management of major depressive disorder</p>
            <a href="/guidelines/2" class="btn">View Details</a>
        </div>
    </body>
    </html>
    """

@app.route('/login')
def login():
    """Route that shows a login form"""
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Login - Medical Reference App</title>
        <style>
            body {{ font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; line-height: 1.6; }}
            h1 {{ color: #2c3e50; border-bottom: 1px solid #eee; padding-bottom: 10px; }}
            .form-group {{ margin-bottom: 15px; }}
            label {{ display: block; margin-bottom: 5px; font-weight: bold; }}
            input[type="text"], input[type="password"] {{ width: 100%; padding: 8px; border: 1px solid #ddd; border-radius: 4px; }}
            .btn {{ display: inline-block; background-color: #3498db; color: white; padding: 8px 16px; 
                   text-decoration: none; border-radius: 4px; border: none; cursor: pointer; }}
            .btn:hover {{ background-color: #2980b9; }}
            .home-link {{ margin-bottom: 20px; }}
        </style>
    </head>
    <body>
        <div class="home-link">
            <a href="/" class="btn">Home</a>
        </div>
        
        <h1>Login</h1>
        
        <form action="/login" method="post">
            <div class="form-group">
                <label for="username">Username:</label>
                <input type="text" id="username" name="username" required>
            </div>
            
            <div class="form-group">
                <label for="password">Password:</label>
                <input type="password" id="password" name="password" required>
            </div>
            
            <div class="form-group">
                <input type="checkbox" id="remember" name="remember">
                <label for="remember" style="display: inline;">Remember me</label>
            </div>
            
            <button type="submit" class="btn">Login</button>
        </form>
        
        <p>Don't have an account? <a href="/register">Register here</a></p>
    </body>
    </html>
    """

@app.route('/register')
def register():
    """Route that shows a registration form"""
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Register - Medical Reference App</title>
        <style>
            body {{ font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; line-height: 1.6; }}
            h1 {{ color: #2c3e50; border-bottom: 1px solid #eee; padding-bottom: 10px; }}
            .form-group {{ margin-bottom: 15px; }}
            label {{ display: block; margin-bottom: 5px; font-weight: bold; }}
            input[type="text"], input[type="email"], input[type="password"] {{ width: 100%; padding: 8px; border: 1px solid #ddd; border-radius: 4px; }}
            .btn {{ display: inline-block; background-color: #3498db; color: white; padding: 8px 16px; 
                   text-decoration: none; border-radius: 4px; border: none; cursor: pointer; }}
            .btn:hover {{ background-color: #2980b9; }}
            .home-link {{ margin-bottom: 20px; }}
        </style>
    </head>
    <body>
        <div class="home-link">
            <a href="/" class="btn">Home</a>
        </div>
        
        <h1>Register</h1>
        
        <form action="/register" method="post">
            <div class="form-group">
                <label for="username">Username:</label>
                <input type="text" id="username" name="username" required>
            </div>
            
            <div class="form-group">
                <label for="email">Email:</label>
                <input type="email" id="email" name="email" required>
            </div>
            
            <div class="form-group">
                <label for="password">Password:</label>
                <input type="password" id="password" name="password" required>
            </div>
            
            <div class="form-group">
                <label for="confirm_password">Confirm Password:</label>
                <input type="password" id="confirm_password" name="confirm_password" required>
            </div>
            
            <button type="submit" class="btn">Register</button>
        </form>
        
        <p>Already have an account? <a href="/login">Login here</a></p>
    </body>
    </html>
    """

@app.route('/health')
def health():
    """Health check endpoint for Render"""
    return jsonify({"status": "healthy"})

# This is the only entry point for the application
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
