import requests
import sys

def test_medication_route(medication_name):
    """Test if a medication page is accessible"""
    url = f"http://127.0.0.1:5000/medication/{medication_name}"
    try:
        response = requests.get(url)
        print(f"Testing URL: {url}")
        print(f"Status code: {response.status_code}")
        print(f"Content length: {len(response.text)} bytes")
        if response.status_code == 200:
            print("SUCCESS: Medication page is accessible")
            return True
        else:
            print(f"ERROR: Received status code {response.status_code}")
            return False
    except Exception as e:
        print(f"ERROR: Failed to connect to {url}")
        print(f"Exception: {str(e)}")
        return False

if __name__ == "__main__":
    # Test a few medication pages
    medications = [
        "Lisinopril",
        "Levetiracetam",
        "Isotretinoin",
        "Fluoxetine (Prozac)",
        "Insulin Glargine"
    ]
    
    success_count = 0
    for medication in medications:
        print(f"\nTesting medication: {medication}")
        if test_medication_route(medication):
            success_count += 1
    
    print(f"\nSummary: {success_count}/{len(medications)} medication pages are accessible")
    
    if success_count == len(medications):
        print("All medication pages are working correctly!")
        sys.exit(0)
    else:
        print("Some medication pages are not accessible!")
        sys.exit(1)
