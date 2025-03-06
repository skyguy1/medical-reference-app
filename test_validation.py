"""
Test script to validate a single condition
"""
from app import app
from validators import validate_condition, validate_medication
import json

def test_condition_validation():
    """Test the validation of a condition"""
    with app.app_context():
        # Test GERD condition
        name = "Gastroesophageal Reflux Disease (GERD)"
        description = "Gastroesophageal reflux disease (GERD) occurs when stomach acid frequently flows back into the tube connecting your mouth and stomach (esophagus)."
        symptoms = [
            "Heartburn", 
            "Regurgitation of food or sour liquid", 
            "Difficulty swallowing", 
            "Sensation of a lump in your throat", 
            "Chronic cough", 
            "Laryngitis", 
            "New or worsening asthma", 
            "Disrupted sleep"
        ]
        treatments = [
            "Lifestyle modifications", 
            "Over-the-counter antacids", 
            "H2 receptor blockers", 
            "Proton pump inhibitors", 
            "Surgery in severe cases"
        ]
        references = [
            {"title": "American College of Gastroenterology Guidelines, 2023", "url": "https://gi.org/"},
            {"title": "American Gastroenterological Association, 2022", "url": "https://gastro.org/"}
        ]
        
        # Convert lists to JSON strings (to simulate how they might be stored in the database)
        symptoms_json = json.dumps(symptoms)
        treatments_json = json.dumps(treatments)
        
        print("Testing with JSON strings:")
        is_valid, errors = validate_condition(name, description, symptoms_json, treatments_json, references)
        print(f"Is valid: {is_valid}")
        print(f"Errors: {errors}")
        
        print("\nTesting with Python lists:")
        is_valid, errors = validate_condition(name, description, symptoms, treatments, references)
        print(f"Is valid: {is_valid}")
        print(f"Errors: {errors}")

if __name__ == "__main__":
    test_condition_validation()
