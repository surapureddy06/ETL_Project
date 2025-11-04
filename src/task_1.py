#imported required packages
import json
from datetime import datetime
from pprint import pprint
import requests
from pathlib import Path
from src.data_templates import patient_template_dict, condition_template_dict
from src.snomed_parent import constraint_parent, expression_constraint
from src.registration import data_dir
import random
#BASE URL for OpenEMR and Primary care website
BASE_URL = "https://in-info-web20.luddy.indianapolis.iu.edu/apis/default/fhir"
BASE_PRIMARY_CARE_URL = "http://137.184.71.65:8080/fhir"

#Retrieves the access token from a local JSON file. Returns the token if found, otherwise returns None.
def get_access_token_from_file():
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

def get_headers(): #Constructs headers for API requests, including the authorization token.
    access_token = get_access_token_from_file()
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    return headers

#Reads the patient resource ID from a local text file. Returns the resource ID if the file exists, otherwise returns None.
def get_patient_resource_id():
    file_path = data_dir / "patient_resource_id.txt"
    try:
        with open(file_path, 'r') as file:
            resource_id = file.read().strip()
            return resource_id
    except FileNotFoundError:
        print(f"Error: {file_path} not found.")
        return None

#Fetches patient details from the FHIR server using the resource ID. Updates the patient template dictionary with fetched data and sends it to the Primary Care FHIR server to create or update the patient resource.
def get_fhir_patient(resource_id):
    url = f'{BASE_URL}/Patient/{resource_id}'
    response = requests.get(url=url, headers=get_headers())
    data = response.json()
    birth_date = data.get('birthDate')
    family_name = data['name'][0]['family']
    given_name = data['name'][0]['given'][0]

    address = data.get('address', [{}])[0]

    line = address.get('line', [''])[0]
    city = address.get('city', '')
    district = address.get('district', 'N/A')
    state = address.get('state', '')
    postal_code = address.get('postalCode', '')
    text = f'{line}, {city}, {state}, {postal_code}'
    unique_patient_id = random.randint(10000, 99999)
    today_date = datetime.today().date().isoformat()
    gender = data.get('gender')

    # Populate the patient template
    patient_template_dict["birthDate"] = birth_date
    patient_template_dict['name'][0]['family'] = family_name
    patient_template_dict['name'][0]['given'][0] = given_name
    patient_template_dict['address'][0]['line'][0] = line
    patient_template_dict['address'][0]['city'] = city
    patient_template_dict['address'][0]['district'] = district
    patient_template_dict['address'][0]['state'] = state
    patient_template_dict['address'][0]['postalCode'] = postal_code
    patient_template_dict['identifier'][0]['period']['start'] = today_date
    patient_template_dict['identifier'][0]['value'] = unique_patient_id
    patient_template_dict['gender'] = gender
    patient_template_dict['address'][0]['text'] = text
    try: # Sends the updated patient data to the Primary Care EHR server
        headers = {
            "Accept": 'application/json'
        }
        url = BASE_PRIMARY_CARE_URL + '/' + 'Patient'
        response = requests.post(url=url, json=patient_template_dict, headers=headers)
        if response.status_code == 200 or response.status_code == 201:
            response_data = response.json()
            new_patient_resource_id = response_data['id']
            with open(data_dir / 'patient_resource_id.txt', 'w') as f: # Saves the new resource ID to a file
                f.write(new_patient_resource_id)
        else:
            print('Error')
    except Exception as e:
        print(e)


def search_condition(patient_resource_id):
    """
    Create a condition resource on Primary Care EHR FHIR Server
    :return:
    """
    # Searches for conditions related to a specific patient resource ID on the FHIR server. Updates the condition template dictionary with hierarchical SNOMED data and sends it to the Primary Care FHIR server.
    url = f'{BASE_URL}/Condition?patient={patient_resource_id}'
    response = requests.get(url=url, headers=get_headers())
    data = response.json()
    if 'entry' in data:
        conditions = data['entry']
        first_condition = conditions[0]
        pprint(first_condition)
        snomed_code_from_openemr = first_condition["resource"]["code"]["coding"][0]["code"]
        ascendant_constraint = constraint_parent(concept_id=snomed_code_from_openemr)
        parent_concept_id = expression_constraint(search_string=ascendant_constraint)[0]
        parent_concept_term = expression_constraint(search_string=ascendant_constraint)[1]

        condition_template_dict["code"]["text"] = parent_concept_term
        condition_template_dict["code"]["coding"][0]["display"] = parent_concept_term
        condition_template_dict["code"]["coding"][0]["code"] = parent_concept_id
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
        condition_template_dict['subject']['reference'] = f"Patient/{primary_care_resource_id}"

        try: # Send the condition data to the Primary Care FHIR server
            headers = {
                "Accept": 'application/json'
            }
            url = BASE_PRIMARY_CARE_URL + '/' + 'Condition'
            response = requests.post(url=url, json=condition_template_dict, headers=headers)
            if response.status_code == 200 or response.status_code == 201:
                response_data = response.json()
                print(response_data)

        except Exception as e:
            print(e)
# Main program execution
if __name__ == '__main__':
    get_fhir_patient(resource_id='985ac7e3-d777-4393-be8d-db0dc7277ba8')
    search_condition(patient_resource_id='985ac7e3-d777-4393-be8d-db0dc7277ba8')
