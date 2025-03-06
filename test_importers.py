"""
Test script for data importers
"""
import logging
from app import app, db
from data_importer_base import BaseDataImporter
from data_importer_cardiology import CardiologyDataImporter
from data_importer_dermatology import DermatologyDataImporter
from data_importer_endocrinology import EndocrinologyDataImporter
from data_importer_gi import GIDataImporter
from data_importer_infectious import InfectiousDataImporter
from data_importer_psychiatry import PsychiatryDataImporter
from data_importer_rheumatology import RheumatologyDataImporter

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_importers():
    """Test all data importers"""
    with app.app_context():
        # Test each importer
        importers = [
            CardiologyDataImporter(),
            DermatologyDataImporter(),
            EndocrinologyDataImporter(),
            GIDataImporter(),
            InfectiousDataImporter(),
            PsychiatryDataImporter(),
            RheumatologyDataImporter()
        ]
        
        for importer in importers:
            logger.info(f"Testing {importer.__class__.__name__}...")
            try:
                importer.import_data()
                logger.info(f"Successfully imported data for {importer.__class__.__name__}")
            except Exception as e:
                logger.error(f"Error importing data for {importer.__class__.__name__}: {str(e)}")

if __name__ == "__main__":
    test_importers()
