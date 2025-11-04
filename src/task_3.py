#Imported required packages
import requests
import json
from pathlib import Path
from src.task_1 import get_patient_resource_id
# Base URL for Primary care EHR website
BASE_PRIMARY_CARE_URL = "http://137.184.71.65:8080/fhir/Observation"
data_dir = Path.cwd() / 'data' # Directory to store JSON files
data_dir.mkdir(exist_ok=True)

#  Observation data
def create_observation_data(patient_resource_id): #Function to generate the observation data structure
    return {
        "resourceType": "Observation",
        "meta": {
            "versionId": "1",
            "lastUpdated": "2024-12-09T17:41:38.679+00:00",
            "source": "#ytTzu9ovGo3hKfow",
            "profile": ["http://hl7.org/fhir/StructureDefinition/vitalsigns"]
        },
        "text": {
            "status": "generated"
        },
        "identifier": [{
            "system": "urn:ietf:rfc:3986",
            "value": "urn:uuid:187e0c12-8dd2-67e2-99b2-bf273c878281"
        }],
        "basedOn": [{
            "identifier": {
                "system": "https://acme.org/identifiers",
                "value": "1234"
            }
        }],
        "status": "final",
        "category": [{
            "coding": [{
                "system": "http://terminology.hl7.org/CodeSystem/observation-category",
                "code": "vital-signs",
                "display": "Vital Signs"
            }]
        }],
        "code": {
            "coding": [{
                "system": "http://loinc.org",
                "code": "85354-9",
                "display": "Blood pressure panel with all children optional"
            }],
            "text": "Blood pressure systolic & diastolic"
        },
        "subject": {
            "reference": f"Patient/{patient_resource_id}"
        },
        "effectiveDateTime": "2012-09-17",
        "performer": [{
            "reference": "Practitioner/4"
        }],
        "interpretation": [{
            "coding": [{
                "system": "http://terminology.hl7.org/CodeSystem/v3-ObservationInterpretation",
                "code": "L",
                "display": "low"
            }],
            "text": "Below low normal"
        }],
        "bodySite": {
            "coding": [{
                "system": "http://snomed.info/sct",
                "code": "368209003",
                "display": "Right arm"
            }]
        },
        "component": [{
            "code": {
                "coding": [{
                    "system": "http://loinc.org",
                    "code": "8480-6",
                    "display": "Systolic blood pressure"
                }, {
                    "system": "http://snomed.info/sct",
                    "code": "271649006",
                    "display": "Systolic blood pressure"
                }, {
                    "system": "http://acme.org/devices/clinical-codes",
                    "code": "bp-s",
                    "display": "Systolic Blood pressure"
                }]
            },
            "valueQuantity": {
                "value": 107,
                "unit": "mmHg",
                "system": "http://unitsofmeasure.org",
                "code": "mm[Hg]"
            },
            "interpretation": [{
                "coding": [{
                    "system": "http://terminology.hl7.org/CodeSystem/v3-ObservationInterpretation",
                    "code": "N",
                    "display": "normal"
                }],
                "text": "Normal"
            }]
        }, {
            "code": {
                "coding": [{
                    "system": "http://loinc.org",
                    "code": "8462-4",
                    "display": "Diastolic blood pressure"
                }]
            },
            "valueQuantity": {
                "value": 60,
                "unit": "mmHg",
                "system": "http://unitsofmeasure.org",
                "code": "mm[Hg]"
            },
            "interpretation": [{
                "coding": [{
                    "system": "http://terminology.hl7.org/CodeSystem/v3-ObservationInterpretation",
                    "code": "L",
                    "display": "low"
                }],
                "text": "Below low normal"
            }]
        }]
    }


def post_data_to_server(observation_data): # Function to post observation data to the API server
    headers = {
        "Content-Type": "application/json",
    }
    try:
        response = requests.post(BASE_PRIMARY_CARE_URL, json=observation_data, headers=headers)
        if response.status_code in [200, 201]:
            print("Observation posted successfully!")
            print("Response:", response.json())
        else:
            print(f"Failed to post observation. Status code: {response.status_code}")
            print("Error:", response.text)
    except requests.exceptions.RequestException as e:
        print("Error during request:", e)


# Main execution
if __name__ == "__main__":
    # Step 1: Read the patient resource ID
    patient_resource_id = get_patient_resource_id()
    print(f"Patient Resource ID: {patient_resource_id}")

    # Step 2: Create observation data with the patient resource ID
    observation_data = create_observation_data(patient_resource_id)

    # Step 3: Post the observation data to the FHIR server
    post_data_to_server(observation_data)
