patient_template_dict = {
    "resourceType": "Patient",
    "identifier": [
        {
            "use": "usual",
            "type": {
                "coding": [
                    {
                        "system": "http://terminology.hl7.org/CodeSystem/v2-0203",
                        "code": "MR"
                    }
                ]
            },
            "system": "urn:oid:1.2.36.146.595.217.0.1",
            "value": "",  ###
            "period": {
                "start": ""  ####
            }
        }
    ],
    "active": True,  ###
    "name": [
        {
            "use": "official",
            "family": "",
            "given": [
                ""
            ]
        }
    ],
    "gender": "",
    "birthDate": "",
    "deceasedBoolean": False,
    "address": [
        {
            "use": "home",
            "type": "both",
            "text": "",
            "line": [
                ""
            ],
            "city": "",
            "district": "",
            "state": "",
            "postalCode": "",
            "period": {
                "start": ""
            }
        }
    ]
}

condition_template_dict = {
    "resourceType": "Condition",
    "clinicalStatus": {
        "coding": [
            {
                "system": "http://terminology.hl7.org/CodeSystem/condition-clinical",
                "code": "active"
            }
        ]
    },
    "verificationStatus": {
        "coding": [
            {
                "system": "http://terminology.hl7.org/CodeSystem/condition-ver-status",
                "code": ""  ##
            }
        ]
    },
    "category": [
        {
            "coding": [
                {
                    "system": "http://terminology.hl7.org/CodeSystem/condition-category",
                    "code": "encounter-diagnosis",
                    "display": "Encounter Diagnosis"
                },
                {
                    "system": "http://snomed.info/sct",
                    "code": "439401001",
                    "display": "Diagnosis"
                }
            ]
        }
    ],
    "severity": {
        "coding": [
            {
                "system": "http://snomed.info/sct",
                "code": "",
                "display": ""
            }
        ]
    },
    "code": {
        "coding": [
            {
                "system": "http://snomed.info/sct",
                "code": "",
                "display": ""
            }
        ],
        "text": ""
    },
    "bodySite": [
        {
            "coding": [
                {
                    "system": "http://snomed.info/sct",
                    "code": "",
                    "display": ""
                }
            ],
            "text": ""
        }
    ],
    "subject": {
        "reference": ""
    },
    "onsetDateTime": ""
}

