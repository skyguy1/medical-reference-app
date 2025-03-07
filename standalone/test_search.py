"""
Test module for search functionality
"""
import unittest
from app import app
from models import db, Condition, Medication, Specialty, Reference, Guideline
from search import search_database
from datetime import datetime, date

class SearchTestCase(unittest.TestCase):
    """Test case for search functionality"""
    
    def setUp(self):
        """Set up test environment"""
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        with app.app_context():
            db.create_all()
            self._create_test_data()
    
    def tearDown(self):
        """Tear down test environment"""
        with app.app_context():
            db.session.remove()
            db.drop_all()
    
    def _create_test_data(self):
        """Create test data for search tests"""
        # Create test conditions
        condition1 = Condition(
            name='Hypertension',
            description='High blood pressure condition',
            symptoms='Headache, dizziness, shortness of breath'
        )
        condition2 = Condition(
            name='Diabetes Mellitus',
            description='Metabolic disorder affecting blood sugar levels',
            symptoms='Increased thirst, frequent urination, fatigue'
        )
        
        # Create test medications
        medication1 = Medication(
            name='Lisinopril',
            description='ACE inhibitor used to treat hypertension',
            drug_class='ACE Inhibitor',
            dosage='10-40 mg daily',
            side_effects='Dry cough, dizziness, headache'
        )
        medication2 = Medication(
            name='Metformin',
            description='Oral medication used to treat type 2 diabetes',
            drug_class='Biguanide',
            dosage='500-2000 mg daily',
            side_effects='Nausea, diarrhea, abdominal discomfort'
        )
        
        # Create test specialties
        specialty1 = Specialty(
            name='Cardiology',
            description='Specialty focused on heart and cardiovascular system'
        )
        specialty2 = Specialty(
            name='Endocrinology',
            description='Specialty focused on hormones and metabolic disorders'
        )
        
        # Create test references
        reference1 = Reference(
            title='Guidelines for Hypertension Management',
            authors='Smith J, Johnson A',
            journal='Journal of Cardiology',
            publication_date=date(2022, 1, 15),
            url='https://example.com/hypertension',
            abstract='Comprehensive guidelines for managing hypertension'
        )
        reference2 = Reference(
            title='Advances in Diabetes Treatment',
            authors='Brown M, Davis R',
            journal='Endocrinology Review',
            publication_date=date(2021, 8, 22),
            url='https://example.com/diabetes',
            abstract='Review of recent advances in diabetes treatment options'
        )
        
        # Create test guidelines
        guideline1 = Guideline(
            title='Hypertension Treatment Protocol',
            organization='American Heart Association',
            publication_date=date(2022, 3, 10),
            summary='Step-by-step protocol for treating hypertension'
        )
        guideline2 = Guideline(
            title='Diabetes Management Guidelines',
            organization='American Diabetes Association',
            publication_date=date(2021, 11, 5),
            summary='Comprehensive guidelines for diabetes management'
        )
        
        # Add all test data to session
        db.session.add_all([
            condition1, condition2,
            medication1, medication2,
            specialty1, specialty2,
            reference1, reference2,
            guideline1, guideline2
        ])
        db.session.commit()
    
    def test_search_conditions(self):
        """Test searching conditions"""
        with app.app_context():
            results, count = search_database(db, 'hypertension', ['Condition'])
            self.assertIn('conditions', results)
            self.assertEqual(len(results['conditions']), 1)
            self.assertEqual(results['conditions'][0].name, 'Hypertension')
            self.assertEqual(count, 1)
    
    def test_search_medications(self):
        """Test searching medications"""
        with app.app_context():
            results, count = search_database(db, 'diabetes', ['Medication'])
            self.assertIn('medications', results)
            self.assertEqual(len(results['medications']), 1)
            self.assertEqual(results['medications'][0].name, 'Metformin')
            self.assertEqual(count, 1)
    
    def test_search_multiple_models(self):
        """Test searching across multiple models"""
        with app.app_context():
            results, count = search_database(
                db, 'hypertension', 
                ['Condition', 'Medication', 'Reference', 'Guideline']
            )
            self.assertEqual(count, 4)  # 1 condition, 1 medication, 1 reference, 1 guideline
            self.assertEqual(len(results['conditions']), 1)
            self.assertEqual(len(results['references']), 1)
            self.assertEqual(len(results['guidelines']), 1)
            # Medication contains "hypertension" in description
            self.assertEqual(len(results['medications']), 1)
    
    def test_search_no_results(self):
        """Test search with no results"""
        with app.app_context():
            results, count = search_database(db, 'nonexistent', ['Condition', 'Medication'])
            self.assertEqual(count, 0)
            self.assertEqual(len(results), 0)
    
    def test_search_case_insensitive(self):
        """Test case-insensitive search"""
        with app.app_context():
            results, count = search_database(db, 'HYPERTENSION', ['Condition'])
            self.assertEqual(count, 1)
            self.assertEqual(results['conditions'][0].name, 'Hypertension')

if __name__ == '__main__':
    unittest.main()
