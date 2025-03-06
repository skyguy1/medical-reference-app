"""
Security Quality Assurance Test

This script tests the security features of the medical reference app.
It verifies that:
1. Password hashing is implemented correctly
2. Protected routes require authentication
3. Input validation prevents common attacks
"""

import os
import sys
import json
import requests
from urllib.parse import urljoin
import re

# Add the current directory to the path so we can import our app modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app, db
from models import User
from werkzeug.security import generate_password_hash, check_password_hash

def run_security_tests():
    """Run security tests"""
    print("\n=== Running Security Tests ===")
    
    # Create a test app context
    with app.app_context():
        test_results = {
            'passed': 0,
            'failed': 0,
            'total': 0
        }
        
        # Test 1: Password hashing
        print("\nTest 1: Password hashing")
        try:
            # Create a user with a hashed password
            password = "TestPassword123!"
            user = User(
                username="securitytestuser",
                email="securitytest@example.com",
                password_hash=generate_password_hash(password)
            )
            db.session.add(user)
            db.session.commit()
            
            # Retrieve the user and check the password hash
            saved_user = User.query.filter_by(username="securitytestuser").first()
            
            # Password should be hashed, not stored in plaintext
            if saved_user.password_hash != password:
                print("✅ PASSED: Password is not stored in plaintext")
                test_results['passed'] += 1
            else:
                print("❌ FAILED: Password is stored in plaintext")
                test_results['failed'] += 1
                
            # Password hash should be verifiable
            if check_password_hash(saved_user.password_hash, password):
                print("✅ PASSED: Password hash is verifiable")
                test_results['passed'] += 1
            else:
                print("❌ FAILED: Password hash is not verifiable")
                test_results['failed'] += 1
                
            test_results['total'] += 2
        except Exception as e:
            print(f"❌ FAILED: Error testing password hashing: {str(e)}")
            test_results['failed'] += 2
            test_results['total'] += 2
        finally:
            # Clean up
            try:
                User.query.filter_by(username="securitytestuser").delete()
                db.session.commit()
            except:
                db.session.rollback()
    
    # Start the Flask app in a separate process for remaining tests
    import subprocess
    import time
    
    # Define the base URL for the API
    base_url = "http://localhost:5000"
    
    # Start the Flask app
    print("\nStarting Flask app for remaining tests...")
    flask_process = subprocess.Popen(
        ["python", "app.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd=os.path.dirname(os.path.abspath(__file__))
    )
    
    # Wait for the app to start
    time.sleep(5)
    
    try:
        # Test 2: Protected routes require authentication
        print("\nTest 2: Protected routes require authentication")
        try:
            # Try to access a protected route without authentication
            response = requests.get(urljoin(base_url, "/visualizations"))
            
            # Should redirect to login page
            if response.status_code == 302 and '/login' in response.url:
                print("✅ PASSED: Protected route redirects to login")
                test_results['passed'] += 1
            else:
                print("❌ FAILED: Protected route does not redirect to login")
                test_results['failed'] += 1
        except Exception as e:
            print(f"❌ FAILED: Error testing protected routes: {str(e)}")
            test_results['failed'] += 1
        finally:
            test_results['total'] += 1
        
        # Test 3: SQL injection prevention
        print("\nTest 3: SQL injection prevention")
        try:
            # Try a SQL injection attack in the search query
            response = requests.get(urljoin(base_url, "/api/search?q=' OR 1=1 --"))
            
            if response.status_code == 200:
                data = response.json()
                # If SQL injection worked, it would return all records
                # We're testing that it doesn't return an excessive number of results
                total_results = data.get('total_results', 0)
                if total_results < 100:  # Arbitrary threshold
                    print("✅ PASSED: SQL injection attempt did not return excessive results")
                    test_results['passed'] += 1
                else:
                    print(f"❌ FAILED: SQL injection may have worked, returned {total_results} results")
                    test_results['failed'] += 1
            else:
                print(f"❌ FAILED: SQL injection test returned status code {response.status_code}")
                test_results['failed'] += 1
        except Exception as e:
            print(f"❌ FAILED: Error testing SQL injection: {str(e)}")
            test_results['failed'] += 1
        finally:
            test_results['total'] += 1
        
        # Test 4: XSS prevention in API responses
        print("\nTest 4: XSS prevention in API responses")
        try:
            # Check if the app escapes HTML in JSON responses
            # This is a basic check - in a real app, we'd need to create data with XSS payloads
            response = requests.get(urljoin(base_url, "/api/search?q=<script>alert('XSS')</script>"))
            
            if response.status_code == 200:
                # The query parameter should be returned in the response
                data = response.json()
                query = data.get('query', '')
                
                # Check if the script tag is present but not executed (it's in a JSON string)
                if '<script>' in query:
                    print("✅ PASSED: XSS payload is returned as data, not executed")
                    test_results['passed'] += 1
                else:
                    print("❌ FAILED: XSS payload is not properly handled")
                    test_results['failed'] += 1
            else:
                print(f"❌ FAILED: XSS test returned status code {response.status_code}")
                test_results['failed'] += 1
        except Exception as e:
            print(f"❌ FAILED: Error testing XSS prevention: {str(e)}")
            test_results['failed'] += 1
        finally:
            test_results['total'] += 1
    
    finally:
        # Stop the Flask app
        print("\nStopping Flask app...")
        flask_process.terminate()
        flask_process.wait()
    
    # Print test summary
    print("\n=== Security Test Summary ===")
    print(f"Total Tests: {test_results['total']}")
    print(f"Passed: {test_results['passed']}")
    print(f"Failed: {test_results['failed']}")
    
    return test_results['passed'] == test_results['total']

if __name__ == '__main__':
    success = run_security_tests()
    sys.exit(0 if success else 1)
