
import requests

# Base URL for the Hermes SNOMED CT API
BASE_HERMES_URL = 'http://159.65.173.51:8080/v1/snomed/concepts'

def get_extended(concept_id):
    """
    Fetches and prints the SNOMED CT concept ID and preferred description term
    for a given SNOMED CT concept ID.
    """
    try:
        url = f'{BASE_HERMES_URL}/{concept_id}'
        response = requests.get(url)
        print(response.url)  # Debugging: Print the request URL

        if response.status_code == 200:
            data = response.json()
            preferred_description = data.get('preferredDescription', {})
            concept_id = data.get("id")
            description_term = preferred_description.get('term', 'No description available')

            print(f"SNOMED Concept ID: {concept_id}")
            print(f"Preferred Description: {description_term}")
        else:
            print(f"Error: Failed to fetch concept details. HTTP Status Code: {response.status_code}")
            print(response.text)
    except requests.RequestException as e:
        print(f"Error: Network error occurred - {e}")


def get_parent_terms_using_ecl(concept_id):
    """
    Use an ECL query to find parent terms for the given SNOMED CT concept ID.
    """
    try:
        # ECL query to search for parent terms of the concept
        ecl_query = f"^ {concept_id} | Concept ID (concept) | "  # ECL query for parents
        url = f'{BASE_HERMES_URL}/search?constraint={ecl_query}'
        response = requests.get(url)
        print(response.url)  # Debugging: Print the request URL

        if response.status_code == 200:
            data = response.json()
            if data:
                print(f"Parent terms for Concept ID {concept_id}:")
                for concept in data:
                    concept_id = concept.get('conceptId')
                    preferred_term = concept.get('preferredDescription', {}).get('term', 'No description available')
                    print(f"Parent Concept ID: {concept_id} | Preferred Term: {preferred_term}")
            else:
                print(f"No parent terms found for Concept ID {concept_id}.")
        else:
            print(f"Error: Failed to fetch parent terms using ECL. HTTP Status Code: {response.status_code}")
            print(response.text)
    except requests.RequestException as e:
        print(f"Error: Network error occurred - {e}")


# Example usage
if __name__ == "__main__":

    snomed_concept_id = "271737000"
    get_extended(concept_id=snomed_concept_id)  # Get extended info for the concept
    get_parent_terms_using_ecl(concept_id=snomed_concept_id)  # Get parent terms using ECL query

    snomed_concept_id = "271737000"
    get_extended(concept_id=snomed_concept_id)

