#Imports required packages
import json
from datetime import datetime
from pprint import pprint

import requests
from pathlib import Path
from src.data_templates import condition_template_dict
from src.snomed_parent import constraint_child, expression_constraint
from src.registration import data_dir
from src.task_1 import get_patient_resource_id
#Base URL for OpenEMR, Primary care EHR and HERMES Website
BASE_URL = "https://in-info-web20.luddy.indianapolis.iu.edu/apis/default/fhir"
BASE_PRIMARY_CARE_URL = "http://137.184.71.65:8080/fhir"
BASE_HERMES_URL = 'http://159.65.173.51:8080/v1/snomed'


def get_access_token_from_file(): # Reads the access token from a JSON file
    file_path = Path(data_dir / "access_token.json")
    if not file_path.exists():
        print("Error: access_token.json file not found.")
        return None
    try:
        with open(file_path, 'r') as json_file:
            json_data = json.load(json_file)
            access_token = json_data.get("access_token")
        return access_token
    except (json.JSONDecodeError, KeyError) as e:
        print(f"Error reading access token from file: {e}")
        return None

def get_headers(): # Constructs the HTTP headers with the access token
    access_token = get_access_token_from_file()
    if not access_token:
        raise ValueError("Access token is missing.")
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    return headers

def search_condition_child(patient_resource_id): # Searches for a condition for a given patient resource ID
    url = f'{BASE_URL}/Condition?patient={patient_resource_id}'
    response = requests.get(url=url, headers=get_headers())
    if response.status_code == 200:
        data = response.json()
        if 'entry' in data: # Retrieves the first condition from the response
            conditions = data['entry']
            first_condition = conditions[0]
            snomed_code_from_openemr = first_condition["resource"]["code"]["coding"][0]["code"]
            print(f"Retrieved SNOMED code from the first condition: {snomed_code_from_openemr}")# Finds child concepts for the SNOMED code

            child_constraint = constraint_child(concept_id=snomed_code_from_openemr)
            child_concept_id, child_concept_term = expression_constraint(search_string=child_constraint)
            print(f"Identified Child Concept ID: {child_concept_id}")
            print(f"Identified Child Preferred Term: {child_concept_term}") # Updates the condition template dictionary with child concept details

            condition_template_dict["code"]["text"] = child_concept_term
            condition_template_dict["code"]["coding"][0]["display"] = child_concept_term
            condition_template_dict["code"]["coding"][0]["code"] = child_concept_id
            condition_template_dict['verificationStatus']['coding'][0]['code'] = first_condition['resource']['verificationStatus']['coding'][0]['code']
            condition_template_dict["severity"]["coding"][0]["system"] = "http://snomed.info/sct"
            condition_template_dict["severity"]["coding"][0]["code"] = "N/A"
            condition_template_dict["severity"]["coding"][0]["display"] = "Not Applicable"
            condition_template_dict["bodySite"][0]["coding"][0]["system"] = "http://snomed.info/sct"
            condition_template_dict["bodySite"][0]["coding"][0]["code"] = "N/A"
            condition_template_dict["bodySite"][0]["coding"][0]["display"] = "Not Applicable"
            condition_template_dict["bodySite"][0]["text"] = "Not Applicable"
            condition_template_dict["onsetDateTime"] = datetime.today().date().isoformat()
            primary_care_resource_id = get_patient_resource_id()
            condition_template_dict['subject']['reference'] = f"Patient/{primary_care_resource_id}" # Posts the updated condition to the Primary Care EHR
            try:
                url = f"{BASE_PRIMARY_CARE_URL}/Condition"
                response = requests.post(url=url, json=condition_template_dict, headers=get_headers())
                if response.status_code in [200, 201]:
                    print("New condition with child concept successfully posted to Primary Care EHR.")
                    print(f"Response Data: {response.json()}")
                else:
                    print(f"Error creating child condition. Status Code: {response.status_code}, Error: {response.text}")
            except Exception as e:
                print(f"Exception during condition creation: {e}")
        else:
            print("No entry key found in data.")
    else:
        print(f"Error fetching conditions. Status Code: {response.status_code}, Error: {response.text}")

# Main execution point of the script
if __name__ == "__main__":
    search_condition_child(patient_resource_id='985ac7e3-d777-4393-be8d-db0dc7277ba8')
