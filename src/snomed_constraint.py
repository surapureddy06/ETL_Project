from pprint import pprint
import requests

BASE_HERMES_URL = 'http://159.65.173.51:8080/v1/snomed'

"""
https://www.hddaccess.com/tips/searching-in-snomed-ct-using-ecl-2
"""


def constraint_1():
    # Search all clinical findings that has an associated morphology of caries and finding site that is a tooth part
    constraint = """
    < 404684003 | Clinical finding (finding) | :
    {
        116676008 |Associated Morphology| = << 65413006 |Caries|
        AND
        363698007 |Finding site| = << 410613002 |Tooth part|
    }
    """
    return constraint


def constraint_2():
    info = "Search all clinical findings that has an associated morphology of caries and finding site that is not a tooth part"
    constraint = """
    < 404684003 | Clinical finding (finding) | :
    {
        116676008 |Associated Morphology| = << 65413006 |Caries|
        AND
        363698007 |Finding site| != << 410613002 |Tooth part|
    }
    """
    return constraint, info


def constraint_3():
    # Search all diseases that has an associated morphology of caries
    constraint = """
    < 64572001 | Disease | : 
    116676008 |Associated Morphology| = << 65413006 |Caries|
    """
    return constraint


def constraint_4():
    # Disorder of mouth with an associated morphology of caries
    constraint = """
    < 118938008 |Disorder of mouth (disorder) | :
    116676008 |Associated Morphology| = << 65413006 |Caries|
    """
    return constraint


def constraint_5():
    # Descendants of Dental caries (disorder)
    constraint = """
    <! 74400008 | Appendicitis |
    """
    return constraint


def constraint_6():
    # Descendants of Caries (morphological abnormality)
    constraint = """
    < 65413006 | Caries |
    """
    return constraint


def constraint_7():
    # Descendants of Disease (morphological abnormality) that has associated morphology of Dental caries
    constraint = """
    < 64572001 | Disease | :
    116676008 | Associated Morphology | = << 65413006 | Caries (morphological abnormality) |
    """
    return constraint


def expression_constraint(search_string):
    response = requests.get(f'{BASE_HERMES_URL}/search?constraint={search_string}')
    data = response.json()
    pprint(data)


if __name__ == '__main__':
    string_value = constraint_5().strip()
    print()
    expression_constraint(search_string=string_value)