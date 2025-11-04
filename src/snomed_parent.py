from pprint import pprint
from wsgiref.util import request_uri

import requests

BASE_HERMES_URL = 'http://159.65.173.51:8080/v1/snomed'


def constraint_parent(concept_id):
    """
    Create an ECL expression constraint to retrieve ascendants of a given SNOMED concept ID.
    """
    constraint = f"""
     >! {concept_id} | Parent |
    """
    return constraint


def constraint_child(concept_id):
    constraint = f"""
     <! {concept_id} | Child |
    """
    return constraint


def expression_constraint(search_string):
    """
    Perform a search using the SNOMED ECL constraint and print the concept ID and preferred term.
    """
    try:
        # Make the request
        response = requests.get(f'{BASE_HERMES_URL}/search?constraint={search_string.strip()}')
        # Handle the response
        if response.status_code == 200:
            data = response.json()
            if len(data) > 0:
                concept_id = data[0]['conceptId']
                concept_preferred_term = data[0]['preferredTerm']
                return concept_id, concept_preferred_term
        else:
            print(f"Error: HTTP Status {response.status_code}")
            pprint(response.json())
    except requests.RequestException as e:
        print(f"Error: Network error occurred - {e}")


if __name__ == '__main__':
    # Specify the SNOMED concept ID
    snomed_concept_id = "74400008"
    ascendant_constraint = constraint_parent(snomed_concept_id)
    print(f"Searching for ascendants of concept ID: {snomed_concept_id}")
    parent_concept_id = expression_constraint(search_string=ascendant_constraint)[0]
    parent_concept_term = expression_constraint(search_string=ascendant_constraint)[1]
    print(f'Parent:{parent_concept_id}')
    print(f'Parent term: {parent_concept_term}')

    child_constraint = constraint_child(concept_id=snomed_concept_id)
    child_terms = expression_constraint(search_string=child_constraint)
    child_concept_id = expression_constraint(search_string=child_constraint)[0]
    child_concept_term = expression_constraint(search_string=child_constraint)[1]
    print(f'Child:{child_concept_id}')
    print(f'Child term: {child_concept_term}')
