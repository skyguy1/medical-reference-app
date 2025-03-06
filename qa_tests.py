"""
Quality Assurance Tests for Medical Reference App

This module contains tests to verify the functionality and integrity of the medical reference app.
It includes three different types of tests:
1. Data Integrity Tests - Verify database consistency and relationships
2. API Endpoint Tests - Test API functionality and responses
3. Security Tests - Check for common security issues
"""

import unittest
import json
import os
import random
import string
import sys
import requests
from datetime import datetime
from flask import Flask
from flask_testing import TestCase
from werkzeug.security import generate_password_hash

# Add the current directory to the path so we can import our app modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app, db
from models import (
    Condition, Medication, Specialty, Reference, Guideline, User,
    ConditionHistory, MedicationHistory, GuidelineHistory, Favorite
)
from utils import safe_json_loads

class DataIntegrityTests(TestCase):
    """Tests for data integrity and database consistency"""
    
    def create_app(self):
        """Create and configure a Flask app for testing"""
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test_medical_reference.db'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        app.config['WTF_CSRF_ENABLED'] = False
        return app
    
    def setUp(self):
        """Set up test database"""
        db.create_all()
        self.seed_test_data()
    
    def tearDown(self):
        """Clean up after tests"""
        db.session.remove()
        db.drop_all()
    
    def seed_test_data(self):
        """Seed the database with test data"""
        # Create specialties
        cardiology = Specialty(name="Cardiology", description="Heart and cardiovascular system")
        neurology = Specialty(name="Neurology", description="Brain and nervous system")
        db.session.add_all([cardiology, neurology])
        db.session.commit()
        
        # Create conditions
        hypertension = Condition(
            name="Hypertension",
            description="High blood pressure",
            symptoms=json.dumps(["Headaches", "Shortness of breath"]),
            treatments=json.dumps(["Medication", "Lifestyle changes"]),
            specialty_id=cardiology.id
        )
        
        stroke = Condition(
            name="Stroke",
            description="Brain damage due to interrupted blood supply",
            symptoms=json.dumps(["Numbness", "Confusion", "Trouble speaking"]),
            treatments=json.dumps(["Emergency care", "Rehabilitation"]),
            specialty_id=neurology.id
        )
        
        db.session.add_all([hypertension, stroke])
        db.session.commit()
        
        # Create medications
        lisinopril = Medication(
            name="Lisinopril",
            class_name="ACE inhibitor",
            description="Medication for hypertension",
            uses=json.dumps(["Hypertension", "Heart failure"]),
            side_effects=json.dumps(["Cough", "Dizziness"]),
            dosing="10-40 mg daily",
            contraindications=json.dumps(["Pregnancy", "History of angioedema"]),
            specialty_id=cardiology.id
        )
        
        aspirin = Medication(
            name="Aspirin",
            class_name="NSAID",
            description="Blood thinner",
            uses=json.dumps(["Pain relief", "Fever reduction", "Blood thinning"]),
            side_effects=json.dumps(["Stomach upset", "Bleeding"]),
            dosing="81-325 mg daily",
            contraindications=json.dumps(["Bleeding disorders", "Aspirin allergy"]),
            specialty_id=cardiology.id
        )
        
        db.session.add_all([lisinopril, aspirin])
        db.session.commit()
        
        # Create references
        reference = Reference(
            title="Hypertension Guidelines",
            authors="Smith J, Johnson A",
            publication="Journal of Hypertension",
            year=2023,
            url="https://example.com/hypertension",
            doi="10.1234/hyp.2023"
        )
        db.session.add(reference)
        db.session.commit()
        
        # Create guidelines
        guideline = Guideline(
            title="Management of Hypertension",
            organization="American Heart Association",
            publication_year=2023,
            summary="Guidelines for managing hypertension",
            url="https://example.com/guidelines/hypertension",
            specialty_id=cardiology.id
        )
        db.session.add(guideline)
        db.session.commit()
        
        # Create user
        user = User(
            username="testuser",
            email="test@example.com",
            password_hash=generate_password_hash("password123")
        )
        db.session.add(user)
        db.session.commit()
        
        # Create relationships
        hypertension.medications.append(lisinopril)
        hypertension.references.append(reference)
        hypertension.guidelines.append(guideline)
        db.session.commit()
    
    def test_condition_relationships(self):
        """Test condition relationships with medications, specialties, etc."""
        condition = Condition.query.filter_by(name="Hypertension").first()
        
        # Test specialty relationship
        self.assertIsNotNone(condition.specialty)
        self.assertEqual(condition.specialty.name, "Cardiology")
        
        # Test medications relationship
        self.assertEqual(len(condition.medications), 1)
        self.assertEqual(condition.medications[0].name, "Lisinopril")
        
        # Test references relationship
        self.assertEqual(len(condition.references), 1)
        self.assertEqual(condition.references[0].title, "Hypertension Guidelines")
        
        # Test guidelines relationship
        self.assertEqual(len(condition.guidelines), 1)
        self.assertEqual(condition.guidelines[0].title, "Management of Hypertension")
    
    def test_medication_relationships(self):
        """Test medication relationships with conditions and specialties"""
        medication = Medication.query.filter_by(name="Lisinopril").first()
        
        # Test specialty relationship
        self.assertIsNotNone(medication.specialty)
        self.assertEqual(medication.specialty.name, "Cardiology")
        
        # Test conditions relationship
        self.assertEqual(len(medication.conditions), 1)
        self.assertEqual(medication.conditions[0].name, "Hypertension")
    
    def test_specialty_relationships(self):
        """Test specialty relationships with conditions and medications"""
        specialty = Specialty.query.filter_by(name="Cardiology").first()
        
        # Test conditions relationship
        self.assertEqual(len(specialty.conditions), 1)
        self.assertEqual(specialty.conditions[0].name, "Hypertension")
        
        # Test medications relationship
        self.assertEqual(len(specialty.medications), 2)
        medication_names = [m.name for m in specialty.medications]
        self.assertIn("Lisinopril", medication_names)
        self.assertIn("Aspirin", medication_names)
    
    def test_history_tracking(self):
        """Test that history records are created when models are updated"""
        # Get a condition to update
        condition = Condition.query.filter_by(name="Hypertension").first()
        
        # Update the condition
        condition.description = "Updated description for testing"
        db.session.commit()
        
        # Check that a history record was created
        history = ConditionHistory.query.filter_by(condition_id=condition.id).all()
        self.assertGreaterEqual(len(history), 1)
        
        # Get a medication to update
        medication = Medication.query.filter_by(name="Lisinopril").first()
        
        # Update the medication
        medication.description = "Updated medication description"
        db.session.commit()
        
        # Check that a history record was created
        history = MedicationHistory.query.filter_by(medication_id=medication.id).all()
        self.assertGreaterEqual(len(history), 1)
    
    def test_json_fields(self):
        """Test that JSON fields are properly stored and retrieved"""
        condition = Condition.query.filter_by(name="Hypertension").first()
        
        # Test symptoms JSON field
        symptoms = safe_json_loads(condition.symptoms, [])
        self.assertIsInstance(symptoms, list)
        self.assertIn("Headaches", symptoms)
        
        # Test treatments JSON field
        treatments = safe_json_loads(condition.treatments, [])
        self.assertIsInstance(treatments, list)
        self.assertIn("Medication", treatments)
        
        # Test medication JSON fields
        medication = Medication.query.filter_by(name="Lisinopril").first()
        uses = safe_json_loads(medication.uses, [])
        self.assertIsInstance(uses, list)
        self.assertIn("Hypertension", uses)
    
    def test_user_favorites(self):
        """Test user favorites functionality"""
        user = User.query.filter_by(username="testuser").first()
        condition = Condition.query.filter_by(name="Hypertension").first()
        
        # Create a favorite
        favorite = Favorite(
            user_id=user.id,
            item_type="condition",
            item_id=condition.id
        )
        db.session.add(favorite)
        db.session.commit()
        
        # Check that the favorite was created
        favorites = Favorite.query.filter_by(user_id=user.id).all()
        self.assertEqual(len(favorites), 1)
        self.assertEqual(favorites[0].item_type, "condition")
        self.assertEqual(favorites[0].item_id, condition.id)


class APIEndpointTests(TestCase):
    """Tests for API endpoints"""
    
    def create_app(self):
        """Create and configure a Flask app for testing"""
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test_medical_reference.db'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        app.config['WTF_CSRF_ENABLED'] = False
        return app
    
    def setUp(self):
        """Set up test database"""
        db.create_all()
        self.seed_test_data()
    
    def tearDown(self):
        """Clean up after tests"""
        db.session.remove()
        db.drop_all()
    
    def seed_test_data(self):
        """Seed the database with test data"""
        # Create specialties
        cardiology = Specialty(name="Cardiology", description="Heart and cardiovascular system")
        db.session.add(cardiology)
        db.session.commit()
        
        # Create conditions
        hypertension = Condition(
            name="Hypertension",
            description="High blood pressure",
            symptoms=json.dumps(["Headaches", "Shortness of breath"]),
            treatments=json.dumps(["Medication", "Lifestyle changes"]),
            specialty_id=cardiology.id
        )
        db.session.add(hypertension)
        db.session.commit()
        
        # Create medications
        lisinopril = Medication(
            name="Lisinopril",
            class_name="ACE inhibitor",
            description="Medication for hypertension",
            uses=json.dumps(["Hypertension", "Heart failure"]),
            side_effects=json.dumps(["Cough", "Dizziness"]),
            dosing="10-40 mg daily",
            contraindications=json.dumps(["Pregnancy", "History of angioedema"]),
            specialty_id=cardiology.id
        )
        db.session.add(lisinopril)
        db.session.commit()
    
    def test_search_api(self):
        """Test the search API endpoint"""
        response = self.client.get('/api/search?q=hypertension')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertIn('results', data)
        self.assertIn('conditions', data['results'])
        
        # Check that we got the hypertension condition in the results
        conditions = data['results']['conditions']
        self.assertEqual(len(conditions), 1)
        self.assertEqual(conditions[0]['name'], 'Hypertension')
    
    def test_conditions_api(self):
        """Test the conditions API endpoint"""
        response = self.client.get('/api/conditions')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertIn('conditions', data)
        self.assertEqual(len(data['conditions']), 1)
        self.assertEqual(data['conditions'][0]['name'], 'Hypertension')
    
    def test_medications_api(self):
        """Test the medications API endpoint"""
        response = self.client.get('/api/medications')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertIn('medications', data)
        self.assertEqual(len(data['medications']), 1)
        self.assertEqual(data['medications'][0]['name'], 'Lisinopril')
    
    def test_specialties_api(self):
        """Test the specialties API endpoint"""
        response = self.client.get('/api/specialties')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertIn('specialties', data)
        self.assertEqual(len(data['specialties']), 1)
        self.assertEqual(data['specialties'][0]['name'], 'Cardiology')
    
    def test_condition_detail_api(self):
        """Test the condition detail API endpoint"""
        condition = Condition.query.filter_by(name="Hypertension").first()
        response = self.client.get(f'/api/conditions/{condition.id}')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertEqual(data['name'], 'Hypertension')
        self.assertEqual(data['description'], 'High blood pressure')
    
    def test_medication_detail_api(self):
        """Test the medication detail API endpoint"""
        medication = Medication.query.filter_by(name="Lisinopril").first()
        response = self.client.get(f'/api/medications/{medication.id}')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertEqual(data['name'], 'Lisinopril')
        self.assertEqual(data['class_name'], 'ACE inhibitor')


class SecurityTests(TestCase):
    """Tests for security features and vulnerabilities"""
    
    def create_app(self):
        """Create and configure a Flask app for testing"""
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test_medical_reference.db'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        app.config['WTF_CSRF_ENABLED'] = False
        return app
    
    def setUp(self):
        """Set up test database"""
        db.create_all()
        self.seed_test_data()
    
    def tearDown(self):
        """Clean up after tests"""
        db.session.remove()
        db.drop_all()
    
    def seed_test_data(self):
        """Seed the database with test data"""
        # Create a test user
        user = User(
            username="testuser",
            email="test@example.com",
            password_hash=generate_password_hash("password123")
        )
        db.session.add(user)
        db.session.commit()
    
    def test_password_hashing(self):
        """Test that passwords are properly hashed"""
        user = User.query.filter_by(username="testuser").first()
        
        # Password should be hashed, not stored in plaintext
        self.assertNotEqual(user.password_hash, "password123")
        
        # Password hash should start with the algorithm identifier
        self.assertTrue(user.password_hash.startswith('pbkdf2:sha256:'))
    
    def test_login_required(self):
        """Test that protected routes require login"""
        # Try to access a protected route without logging in
        response = self.client.get('/visualizations')
        
        # Should redirect to login page
        self.assertEqual(response.status_code, 302)
        self.assertTrue('/login' in response.location)
    
    def test_sql_injection_resistance(self):
        """Test resistance to SQL injection attacks"""
        # Try a simple SQL injection attack in the search query
        response = self.client.get("/api/search?q=' OR 1=1 --")
        self.assertEqual(response.status_code, 200)
        
        # The search should not return all records
        data = json.loads(response.data)
        self.assertEqual(len(data['results']['conditions']), 0)
    
    def test_xss_resistance(self):
        """Test resistance to cross-site scripting (XSS) attacks"""
        # Create a condition with a potential XSS payload
        xss_condition = Condition(
            name="<script>alert('XSS')</script>",
            description="Test for XSS vulnerabilities",
            symptoms=json.dumps(["<img src=x onerror=alert('XSS')>"]),
            treatments=json.dumps(["<a href='javascript:alert(\"XSS\")'>Click me</a>"])
        )
        db.session.add(xss_condition)
        db.session.commit()
        
        # Get the condition via the API
        response = self.client.get(f'/api/conditions/{xss_condition.id}')
        self.assertEqual(response.status_code, 200)
        
        # The response should contain the escaped HTML
        data = json.loads(response.data)
        self.assertEqual(data['name'], "<script>alert('XSS')</script>")
        
        # The symptoms and treatments should be JSON strings
        symptoms = json.loads(data['symptoms'])
        self.assertEqual(symptoms[0], "<img src=x onerror=alert('XSS')>")


def run_tests():
    """Run all tests"""
    # Create test suites
    data_suite = unittest.TestLoader().loadTestsFromTestCase(DataIntegrityTests)
    api_suite = unittest.TestLoader().loadTestsFromTestCase(APIEndpointTests)
    security_suite = unittest.TestLoader().loadTestsFromTestCase(SecurityTests)
    
    # Create a test runner
    runner = unittest.TextTestRunner(verbosity=2)
    
    # Run the tests
    print("\n=== Running Data Integrity Tests ===")
    data_result = runner.run(data_suite)
    
    print("\n=== Running API Endpoint Tests ===")
    api_result = runner.run(api_suite)
    
    print("\n=== Running Security Tests ===")
    security_result = runner.run(security_suite)
    
    # Print summary
    print("\n=== Test Summary ===")
    print(f"Data Integrity Tests: {data_result.testsRun} run, {len(data_result.errors)} errors, {len(data_result.failures)} failures")
    print(f"API Endpoint Tests: {api_result.testsRun} run, {len(api_result.errors)} errors, {len(api_result.failures)} failures")
    print(f"Security Tests: {security_result.testsRun} run, {len(security_result.errors)} errors, {len(security_result.failures)} failures")
    
    # Return True if all tests passed, False otherwise
    return (len(data_result.errors) + len(data_result.failures) + 
            len(api_result.errors) + len(api_result.failures) + 
            len(security_result.errors) + len(security_result.failures)) == 0


if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)
