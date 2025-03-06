"""
API Functionality Quality Assurance Test

This script tests the API functionality of the medical reference app.
It verifies that:
1. API endpoints return the expected status codes
2. API responses contain the expected data
3. Search functionality works correctly
"""

import os
import sys
import json
import requests
from urllib.parse import urljoin

# Add the current directory to the path so we can import our app modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def run_api_functionality_tests():
    """Run API functionality tests"""
    print("\n=== Running API Functionality Tests ===")
    
    # Start the Flask app in a separate process
    import subprocess
    import time
    import signal
    
    # Define the base URL for the API
    base_url = "http://localhost:5000"
    
    # Start the Flask app
    print("Starting Flask app...")
    flask_process = subprocess.Popen(
        ["python", "app.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd=os.path.dirname(os.path.abspath(__file__))
    )
    
    # Wait for the app to start
    time.sleep(5)
    
    test_results = {
        'passed': 0,
        'failed': 0,
        'total': 0
    }
    
    try:
        # Test 1: Check that the API is running
        print("\nTest 1: Check that the API is running")
        try:
            response = requests.get(urljoin(base_url, "/"))
            if response.status_code == 200:
                print("✅ PASSED: API is running")
                test_results['passed'] += 1
            else:
                print(f"❌ FAILED: API returned status code {response.status_code}")
                test_results['failed'] += 1
        except Exception as e:
            print(f"❌ FAILED: Error connecting to API: {str(e)}")
            test_results['failed'] += 1
        finally:
            test_results['total'] += 1
        
        # Test 2: Check the search API
        print("\nTest 2: Check the search API")
        try:
            response = requests.get(urljoin(base_url, "/api/search?q=hypertension"))
            if response.status_code == 200:
                data = response.json()
                if 'results' in data and 'conditions' in data['results']:
                    print("✅ PASSED: Search API returned expected structure")
                    test_results['passed'] += 1
                else:
                    print("❌ FAILED: Search API did not return expected structure")
                    test_results['failed'] += 1
            else:
                print(f"❌ FAILED: Search API returned status code {response.status_code}")
                test_results['failed'] += 1
        except Exception as e:
            print(f"❌ FAILED: Error with search API: {str(e)}")
            test_results['failed'] += 1
        finally:
            test_results['total'] += 1
        
        # Test 3: Check the conditions API
        print("\nTest 3: Check the conditions API")
        try:
            response = requests.get(urljoin(base_url, "/api/conditions"))
            if response.status_code == 200:
                data = response.json()
                if 'conditions' in data and isinstance(data['conditions'], list):
                    print("✅ PASSED: Conditions API returned expected structure")
                    test_results['passed'] += 1
                else:
                    print("❌ FAILED: Conditions API did not return expected structure")
                    test_results['failed'] += 1
            else:
                print(f"❌ FAILED: Conditions API returned status code {response.status_code}")
                test_results['failed'] += 1
        except Exception as e:
            print(f"❌ FAILED: Error with conditions API: {str(e)}")
            test_results['failed'] += 1
        finally:
            test_results['total'] += 1
        
        # Test 4: Check the medications API
        print("\nTest 4: Check the medications API")
        try:
            response = requests.get(urljoin(base_url, "/api/medications"))
            if response.status_code == 200:
                data = response.json()
                if 'medications' in data and isinstance(data['medications'], list):
                    print("✅ PASSED: Medications API returned expected structure")
                    test_results['passed'] += 1
                else:
                    print("❌ FAILED: Medications API did not return expected structure")
                    test_results['failed'] += 1
            else:
                print(f"❌ FAILED: Medications API returned status code {response.status_code}")
                test_results['failed'] += 1
        except Exception as e:
            print(f"❌ FAILED: Error with medications API: {str(e)}")
            test_results['failed'] += 1
        finally:
            test_results['total'] += 1
        
        # Test 5: Check the specialties API
        print("\nTest 5: Check the specialties API")
        try:
            response = requests.get(urljoin(base_url, "/api/specialties"))
            if response.status_code == 200:
                data = response.json()
                if 'specialties' in data and isinstance(data['specialties'], list):
                    print("✅ PASSED: Specialties API returned expected structure")
                    test_results['passed'] += 1
                else:
                    print("❌ FAILED: Specialties API did not return expected structure")
                    test_results['failed'] += 1
            else:
                print(f"❌ FAILED: Specialties API returned status code {response.status_code}")
                test_results['failed'] += 1
        except Exception as e:
            print(f"❌ FAILED: Error with specialties API: {str(e)}")
            test_results['failed'] += 1
        finally:
            test_results['total'] += 1
    
    finally:
        # Stop the Flask app
        print("\nStopping Flask app...")
        flask_process.terminate()
        flask_process.wait()
    
    # Print test summary
    print("\n=== API Functionality Test Summary ===")
    print(f"Total Tests: {test_results['total']}")
    print(f"Passed: {test_results['passed']}")
    print(f"Failed: {test_results['failed']}")
    
    return test_results['passed'] == test_results['total']

if __name__ == '__main__':
    success = run_api_functionality_tests()
    sys.exit(0 if success else 1)
