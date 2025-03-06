"""
Script to forcefully reset the database by dropping all tables and recreating them
"""
import os
import sys
from datetime import datetime

# Set up the Flask app context
from app import app, db
from models import Condition, Medication, Reference, Specialty, Guideline

def reset_database():
    """Reset the database by dropping all tables and recreating them"""
    with app.app_context():
        print("Dropping all tables...")
        db.drop_all()
        
        print("Creating all tables...")
        db.create_all()
        
        print("Database reset complete!")

if __name__ == "__main__":
    reset_database()
