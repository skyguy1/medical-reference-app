#!/usr/bin/env python
"""
Dependency verification script for Medical Reference App
This script verifies that installed package versions match the expected versions
and will exit with an error if incompatible versions are detected.
"""
import sys
import pkg_resources
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Critical dependencies that must be exactly matched
CRITICAL_DEPENDENCIES = {
    'flask': '2.0.1',
    'werkzeug': '2.0.1',
    'jinja2': '3.0.1',
    'itsdangerous': '2.0.1',
    'sqlalchemy': '1.4.23',
    'flask-sqlalchemy': '2.5.1',
    'flask-login': '0.5.0',
    'markupsafe': '2.0.1',
    'click': '8.0.1',
}

def verify_dependencies():
    """Verify that installed packages match expected versions"""
    logger.info("Verifying dependency versions...")
    
    # Get installed packages
    installed_packages = {pkg.key: pkg.version for pkg in pkg_resources.working_set}
    
    # Check critical dependencies
    errors = []
    for package, expected_version in CRITICAL_DEPENDENCIES.items():
        if package in installed_packages:
            installed_version = installed_packages[package]
            if installed_version != expected_version:
                error_msg = f"Version mismatch for {package}: expected {expected_version}, got {installed_version}"
                errors.append(error_msg)
                logger.error(error_msg)
        else:
            error_msg = f"Missing critical dependency: {package}"
            errors.append(error_msg)
            logger.error(error_msg)
    
    # Report results
    if errors:
        logger.error(f"Dependency verification failed with {len(errors)} errors")
        return False
    else:
        logger.info("All dependencies verified successfully")
        return True

if __name__ == "__main__":
    if not verify_dependencies():
        sys.exit(1)  # Exit with error code
    sys.exit(0)  # Exit successfully
