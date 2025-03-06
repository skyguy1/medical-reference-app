"""
Data Validation Quality Assurance Test

This script tests the data validation functionality of the medical reference app.
It verifies that:
1. Required fields are properly enforced
2. Field types are validated
3. Relationships between models are maintained
"""

import os
import sys
import json
from datetime import datetime

# Add the current directory to the path so we can import our app modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app, db
from models import Condition, Medication, Specialty, Reference, Guideline, User

def run_data_validation_tests():
    """Run data validation tests"""
    print("\n=== Running Data Validation Tests ===")
    
    # Create a test app context
    with app.app_context():
        test_results = {
            'passed': 0,
            'failed': 0,
            'total': 0
        }
        
        # Test 1: Validate required fields for Condition
        print("\nTest 1: Validate required fields for Condition")
        try:
            # Try to create a condition without a name (required field)
            condition = Condition(description="Test description")
            db.session.add(condition)
            db.session.commit()
            print("❌ FAILED: Created condition without required name field")
            test_results['failed'] += 1
        except Exception as e:
            print(f"✅ PASSED: Properly rejected condition without name: {str(e)}")
            test_results['passed'] += 1
        finally:
            db.session.rollback()
            test_results['total'] += 1
        
        # Test 2: Validate JSON fields
        print("\nTest 2: Validate JSON fields")
        try:
            # Create a condition with valid JSON fields
            condition = Condition(
                name="Test Condition",
                description="Test description",
                symptoms=json.dumps(["Symptom 1", "Symptom 2"]),
                treatments=json.dumps(["Treatment 1", "Treatment 2"])
            )
            db.session.add(condition)
            db.session.commit()
            
            # Retrieve the condition and check JSON fields
            saved_condition = Condition.query.filter_by(name="Test Condition").first()
            symptoms = json.loads(saved_condition.symptoms)
            treatments = json.loads(saved_condition.treatments)
            
            if isinstance(symptoms, list) and isinstance(treatments, list):
                print("✅ PASSED: JSON fields properly stored and retrieved")
                test_results['passed'] += 1
            else:
                print("❌ FAILED: JSON fields not properly stored or retrieved")
                test_results['failed'] += 1
        except Exception as e:
            print(f"❌ FAILED: Error handling JSON fields: {str(e)}")
            test_results['failed'] += 1
        finally:
            db.session.rollback()
            test_results['total'] += 1
        
        # Test 3: Validate relationships
        print("\nTest 3: Validate relationships")
        try:
            # Create a specialty
            specialty = Specialty(name="Test Specialty", description="Test specialty description")
            db.session.add(specialty)
            db.session.commit()
            
            # Create a condition with the specialty
            condition = Condition(
                name="Test Condition",
                description="Test description",
                specialty_id=specialty.id
            )
            db.session.add(condition)
            db.session.commit()
            
            # Retrieve the condition and check the relationship
            saved_condition = Condition.query.filter_by(name="Test Condition").first()
            if saved_condition.specialty and saved_condition.specialty.name == "Test Specialty":
                print("✅ PASSED: Relationship properly established")
                test_results['passed'] += 1
            else:
                print("❌ FAILED: Relationship not properly established")
                test_results['failed'] += 1
        except Exception as e:
            print(f"❌ FAILED: Error handling relationships: {str(e)}")
            test_results['failed'] += 1
        finally:
            db.session.rollback()
            test_results['total'] += 1
        
        # Clean up any test data
        try:
            Condition.query.filter_by(name="Test Condition").delete()
            Specialty.query.filter_by(name="Test Specialty").delete()
            db.session.commit()
        except:
            db.session.rollback()
        
        # Print test summary
        print("\n=== Data Validation Test Summary ===")
        print(f"Total Tests: {test_results['total']}")
        print(f"Passed: {test_results['passed']}")
        print(f"Failed: {test_results['failed']}")
        
        return test_results['passed'] == test_results['total']

if __name__ == '__main__':
    success = run_data_validation_tests()
    sys.exit(0 if success else 1)
