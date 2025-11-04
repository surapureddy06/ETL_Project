import json
import requests
from pprint import pprint
import matplotlib.pyplot as plt
from pathlib import Path
from datetime import datetime
from src.registration import data_dir

# Correct API Base URL
BASE_URL = "https://in-info-web20.luddy.indianapolis.iu.edu/apis/default/fhir"

def get_access_token_from_file():
    """
    Reads the access token from a file.
    """
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

def get_headers():
    """
    Constructs the headers for API requests using the access token.
    """
    access_token = get_access_token_from_file()
    if not access_token:
        print("Access token is missing. Ensure access_token.json is properly set up.")
        return None
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    return headers

def get_all_patients():
    """
    Fetches all patients from the FHIR server, handling pagination if needed.
    """
    url = f'{BASE_URL}/Patient'
    patients = []
    headers = get_headers()
    if not headers:
        print("Failed to construct headers. Exiting...")
        return []

    while url:
        try:
            # Increase timeout to 180 seconds
            response = requests.get(url=url, headers=headers, timeout=180)
            print(f"Requesting URL: {url}")
            print(f"Response Status Code: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                if 'entry' in data:
                    patients.extend(data['entry'])
                # Check for pagination and get the next URL
                url = data.get('link', [{}])[-1].get('url') if data.get('link') else None
            else:
                print(f"Failed to retrieve patients. Status code: {response.status_code}")
                print(f"Response Text: {response.text}")
                break
        except requests.exceptions.Timeout:
            print("Request timed out. Please check the server or your network connection.")
            break
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            break
        except json.JSONDecodeError:
            print(f"Error decoding JSON from the response. Response text: {response.text}")
            break
    return patients

def calculate_age(birth_date):
    """
    Calculates the age based on the birth date.
    """
    birth_date = datetime.strptime(birth_date, '%Y-%m-%d')
    today = datetime.today()
    age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
    return age

def plot_patient_ages():
    """
    Plots a histogram of patient ages.
    """
    patients = get_all_patients()
    if not patients:
        print("No patients retrieved from the server. Exiting...")
        return

    ages = []
    for patient in patients:
        birth_date = patient['resource'].get('birthDate')
        if birth_date:
            age = calculate_age(birth_date)
            ages.append(age)

    if not ages:
        print("No patient ages found to plot.")
        return

    # Plotting the age distribution
    plt.figure(figsize=(10, 6))
    plt.hist(ages, bins=range(0, 100, 5), edgecolor='black', alpha=0.7)
    plt.title("Age Distribution of Patients")
    plt.xlabel("Age (years)")
    plt.ylabel("Frequency")
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.show()

if __name__ == '_main_':
    plot_patient_ages()