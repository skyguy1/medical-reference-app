"""
Base Data Importer

This module provides a base class for importing medical data into the database.
"""
from models import db, Condition, Medication, Specialty, Reference, Guideline
from validators import validate_condition, validate_medication, validate_reference, validate_guideline
import logging
from sqlalchemy.exc import SQLAlchemyError

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='data_import.log',
    filemode='a'
)
logger = logging.getLogger('data_importer')

class BaseDataImporter:
    """
    Base class for importing medical data into the database
    """
    
    def __init__(self, specialty_name, specialty_description):
        """
        Initialize the data importer with specialty information
        
        Args:
            specialty_name: Name of the medical specialty
            specialty_description: Description of the medical specialty
        """
        self.specialty_name = specialty_name
        self.specialty_description = specialty_description
        self.specialty = self._get_or_create_specialty()
        self.transaction_errors = []
        
    def _get_or_create_specialty(self):
        """
        Get or create the specialty in the database
        
        Returns:
            Specialty: The specialty object
        """
        specialty = Specialty.query.filter_by(name=self.specialty_name).first()
        if not specialty:
            specialty = Specialty(name=self.specialty_name, description=self.specialty_description)
            try:
                db.session.add(specialty)
                db.session.commit()
                logger.info(f"Created specialty: {self.specialty_name}")
            except SQLAlchemyError as e:
                db.session.rollback()
                logger.error(f"Error creating specialty: {str(e)}")
                raise
        return specialty
    
    def add_condition(self, name, description, symptoms, treatments, references=None):
        """
        Add a condition to the database
        
        Args:
            name: Name of the condition
            description: Description of the condition
            symptoms: List of symptoms
            treatments: List of treatments
            references: List of references
            
        Returns:
            Condition: The created condition object or None if validation fails
        """
        # Ensure references is a list
        if references is None:
            references = []
        
        # Ensure symptoms and treatments are Python lists, not JSON strings
        if isinstance(symptoms, str):
            try:
                import json
                symptoms = json.loads(symptoms)
            except json.JSONDecodeError:
                logger.error(f"Invalid JSON format for symptoms: {symptoms}")
                symptoms = [symptoms]  # Convert to a single-item list as fallback
        
        if isinstance(treatments, str):
            try:
                import json
                treatments = json.loads(treatments)
            except json.JSONDecodeError:
                logger.error(f"Invalid JSON format for treatments: {treatments}")
                treatments = [treatments]  # Convert to a single-item list as fallback
        
        # Validate condition data
        print(f"Validating condition: {name}")
        print(f"  Description: {description[:50]}...")
        print(f"  Symptoms type: {type(symptoms)}")
        print(f"  Treatments type: {type(treatments)}")
        print(f"  References type: {type(references)}")
        
        is_valid, errors = validate_condition(name, description, symptoms, treatments, references)
        if not is_valid:
            logger.warning(f"Validation failed for condition {name}: {errors}")
            self.transaction_errors.append(f"Validation failed for condition {name}: {errors}")
            print(f"Validation failed for condition {name}: {errors}")
            return None
            
        # Check if condition already exists
        condition = Condition.query.filter_by(name=name).first()
        if not condition:
            try:
                # Convert lists to JSON strings for database storage
                import json
                symptoms_json = json.dumps(symptoms)
                treatments_json = json.dumps(treatments)
                
                # Start transaction
                condition = Condition(
                    name=name,
                    description=description,
                    symptoms=symptoms_json,
                    treatments=treatments_json,
                    specialty=self.specialty
                )
                db.session.add(condition)
                
                # Add references if provided
                if references:
                    for ref_data in references:
                        ref_title = ref_data.get('title')
                        ref_url = ref_data.get('url')
                        if ref_title:
                            reference = Reference.query.filter_by(title=ref_title).first()
                            if not reference:
                                reference = Reference(title=ref_title, url=ref_url)
                                db.session.add(reference)
                            condition.references.append(reference)
                
                # Commit transaction
                db.session.commit()
                logger.info(f"Added condition: {name}")
                return condition
            except SQLAlchemyError as e:
                db.session.rollback()
                logger.error(f"Error adding condition {name}: {str(e)}")
                self.transaction_errors.append(f"Error adding condition {name}: {str(e)}")
                return None
        else:
            logger.info(f"Condition already exists: {name}")
            return condition
    
    def add_medication(self, name, class_name, uses, side_effects, dosing, contraindications, description=None):
        """
        Add a medication to the database
        
        Args:
            name: Name of the medication
            class_name: Class of the medication
            uses: Uses of the medication
            side_effects: Side effects of the medication
            dosing: Dosing information
            contraindications: Contraindications
            description: Description of the medication
        
        Returns:
            Medication: The created medication object or None if validation fails
        """
        # Ensure uses, side_effects, and contraindications are Python lists
        if isinstance(uses, str):
            try:
                import json
                uses = json.loads(uses)
            except json.JSONDecodeError:
                logger.error(f"Invalid JSON format for uses: {uses}")
                uses = [uses]  # Convert to a single-item list as fallback
    
        if isinstance(side_effects, str):
            try:
                import json
                side_effects = json.loads(side_effects)
            except json.JSONDecodeError:
                logger.error(f"Invalid JSON format for side_effects: {side_effects}")
                side_effects = [side_effects]  # Convert to a single-item list as fallback
    
        if isinstance(contraindications, str):
            try:
                import json
                contraindications = json.loads(contraindications)
            except json.JSONDecodeError:
                logger.error(f"Invalid JSON format for contraindications: {contraindications}")
                contraindications = [contraindications]  # Convert to a single-item list as fallback
    
        # Validate medication data
        is_valid, errors = validate_medication(name, class_name, uses, side_effects, dosing, contraindications)
        if not is_valid:
            logger.warning(f"Validation failed for medication {name}: {errors}")
            self.transaction_errors.append(f"Validation failed for medication {name}: {errors}")
            return None
        
        # Check if medication already exists
        medication = Medication.query.filter_by(name=name).first()
        if not medication:
            try:
                # Convert lists to JSON strings for database storage
                import json
                uses_json = json.dumps(uses)
                side_effects_json = json.dumps(side_effects)
                contraindications_json = json.dumps(contraindications)
                
                # Start transaction
                medication = Medication(
                    name=name,
                    class_name=class_name,
                    uses=uses_json,
                    side_effects=side_effects_json,
                    dosing=dosing,
                    contraindications=contraindications_json,
                    specialty=self.specialty,
                    description=description or ""  # Add the description field with a default empty string
                )
                db.session.add(medication)
                db.session.commit()
                logger.info(f"Added medication: {name}")
                return medication
            except SQLAlchemyError as e:
                db.session.rollback()
                logger.error(f"Error adding medication {name}: {str(e)}")
                self.transaction_errors.append(f"Error adding medication {name}: {str(e)}")
                return None
        else:
            logger.info(f"Medication already exists: {name}")
            return medication
    
    def add_reference(self, title, url=None, authors=None, publication=None, year=None, doi=None, description=None):
        """
        Add a reference to the database
        
        Args:
            title: Title of the reference
            url: URL of the reference
            authors: Authors of the reference
            publication: Publication name
            year: Publication year
            doi: Digital Object Identifier
            description: Description of the reference
            
        Returns:
            Reference: The created reference object or None if validation fails
        """
        # Validate reference data
        is_valid, errors = validate_reference(title, url, authors, publication, year, doi)
        if not is_valid:
            logger.warning(f"Validation failed for reference {title}: {errors}")
            self.transaction_errors.append(f"Validation failed for reference {title}: {errors}")
            return None
            
        # Check if reference already exists
        reference = Reference.query.filter_by(title=title).first()
        if not reference:
            try:
                # Start transaction
                reference = Reference(
                    title=title,
                    url=url,
                    authors=authors,
                    publication=publication,
                    year=year,
                    doi=doi,
                    description=description
                )
                db.session.add(reference)
                db.session.commit()
                logger.info(f"Added reference: {title}")
                return reference
            except SQLAlchemyError as e:
                db.session.rollback()
                logger.error(f"Error adding reference {title}: {str(e)}")
                self.transaction_errors.append(f"Error adding reference {title}: {str(e)}")
                return None
        else:
            logger.info(f"Reference already exists: {title}")
            return reference
    
    def add_guideline(self, title, organization, publication_year, summary, url=None):
        """
        Add a guideline to the database
        
        Args:
            title: Title of the guideline
            organization: Organization that published the guideline
            publication_year: Year the guideline was published
            summary: Summary of the guideline
            url: URL of the guideline
            
        Returns:
            Guideline: The created guideline object or None if validation fails
        """
        # Validate guideline data
        is_valid, errors = validate_guideline(title, organization, publication_year, summary, url)
        if not is_valid:
            logger.warning(f"Validation failed for guideline {title}: {errors}")
            self.transaction_errors.append(f"Validation failed for guideline {title}: {errors}")
            return None
            
        # Check if guideline already exists
        guideline = Guideline.query.filter_by(title=title).first()
        if not guideline:
            try:
                # Start transaction
                guideline = Guideline(
                    title=title,
                    organization=organization,
                    publication_year=publication_year,
                    summary=summary,
                    url=url,
                    specialty=self.specialty
                )
                db.session.add(guideline)
                db.session.commit()
                logger.info(f"Added guideline: {title}")
                return guideline
            except SQLAlchemyError as e:
                db.session.rollback()
                logger.error(f"Error adding guideline {title}: {str(e)}")
                self.transaction_errors.append(f"Error adding guideline {title}: {str(e)}")
                return None
        else:
            logger.info(f"Guideline already exists: {title}")
            return guideline
            
    def link_medication_to_condition(self, medication_name, condition_name):
        """
        Link a medication to a condition in the database
        
        Args:
            medication_name: Name of the medication
            condition_name: Name of the condition
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Get the medication and condition
            medication = Medication.query.filter_by(name=medication_name).first()
            condition = Condition.query.filter_by(name=condition_name).first()
            
            # Check if both medication and condition exist
            if not medication:
                logger.warning(f"Medication not found: {medication_name}")
                self.transaction_errors.append(f"Medication not found: {medication_name}")
                return False
                
            if not condition:
                logger.warning(f"Condition not found: {condition_name}")
                self.transaction_errors.append(f"Condition not found: {condition_name}")
                return False
                
            # Check if the medication is already linked to the condition
            if condition in medication.conditions:
                logger.info(f"Medication {medication_name} already linked to condition {condition_name}")
                return True
                
            # Link the medication to the condition
            medication.conditions.append(condition)
            db.session.commit()
            logger.info(f"Linked medication {medication_name} to condition {condition_name}")
            return True
            
        except SQLAlchemyError as e:
            db.session.rollback()
            logger.error(f"Error linking medication {medication_name} to condition {condition_name}: {str(e)}")
            self.transaction_errors.append(f"Error linking medication {medication_name} to condition {condition_name}: {str(e)}")
            return False
            
    def get_transaction_errors(self):
        """
        Get all transaction errors that occurred during data import
        
        Returns:
            list: List of error messages
        """
        return self.transaction_errors
