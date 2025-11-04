#Imported required packages
import requests
import json
from pathlib import Path
from src.task_1 import get_patient_resource_id
# Base URL for Primary care EHR website
BASE_PRIMARY_CARE_URL = "http://137.184.71.65:8080/fhir/Procedure"
# Directory to store JSON files
data_dir = Path.cwd() / 'data'
data_dir.mkdir(exist_ok=True)
# Creates the 'data' directory if it doesn't exist
#Function to create a Procedure data structure
def create_procedure_data(patient_resource_id):
    return {
        "resourceType": "Procedure",

        "meta": {
            "versionId": "1",
            "lastUpdated": "2024-12-09T17:41:39.049+00:00",
            "source": "#Obb5mhH5jY5H9V3m"
        },
        "text": {
            "status": "generated"
        },
        "status": "completed",
        "code": {
            "coding": [{
                "system": "http://snomed.info/sct",
                "code": "74400008",
                "display": "Appendectomy (Procedure)"
            }],
            "text": "Appendectomy"
        },
        "subject": {
            "reference": f"Patient/{patient_resource_id}"  # Dynamic reference
        },
        "recorder": {
            "reference": "Practitioner/4",
            "display": "Dr Adam Careful"
        },
        "performer": [{
            "actor": {
                "reference": "Practitioner/4",
                "display": "Dr Adam Careful"
            }
        }],
        "followUp": [{
            "text": "ROS 5 days  - 2024-04-12"
        }],
        "note": [{
            "text": "Routine Appendectomy. Appendix was inflamed and in retro-caecal position"
        }]
    }

# Function to POST JSON data to an API
def post_data_to_server(procedure_data):
    headers = {
        "Content-Type": "application/json",
    }
    try:
        # Sends the POST request with procedure data
        response = requests.post(BASE_PRIMARY_CARE_URL, json=procedure_data, headers=headers)
        if response.status_code in [200, 201]:
            print("Procedure posted successfully!")
            print("Response:", response.json())
        else:
            print(f"Failed to post procedure. Status code: {response.status_code}")
            print("Error:", response.text)
    except requests.exceptions.RequestException as e:
        print("Error during request:", e)

# Main execution
if __name__ == "__main__":
    # Step 1: Reads the patient resource ID
    patient_resource_id = get_patient_resource_id()
    print(f"Patient Resource ID: {patient_resource_id}")

    # Step 2: Create procedure data with the patient resource ID
    procedure_data = create_procedure_data(patient_resource_id)

    # Step 3: Post the procedure data to the FHIR server
    post_data_to_server(procedure_data)
