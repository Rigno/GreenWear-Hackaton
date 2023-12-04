import requests
from core.models import FACTORY_LOCATION


'''
API REQUEST:
-----------------------------------------------------------------------------------
Suppose that we ship our merch directly from the factory,we just need to define 
the shipping location (when the user will buy our merch) and the materials location.
Material wights are from 1 (non influent) to 3.
'''

def calculate_footprints(materials):
    
    url = 'http://194.233.164.36/api/calculateCO2'
    headers = {
        'x-tenant': 'greenwear',
        'x-apikey': 'XNwtvpHY6skocyd+0B+I1w4p51oWdxXEjREEpa9LPcE=',
    }

    payload = {
        "transport": {
            "shippingFrom": "{0};{1}".format(FACTORY_LOCATION[0], FACTORY_LOCATION[1]),
            "shippingTo": "0;0"
        },
        "production": []
    }
    
    for material in materials:
        value = {
            "materialLocation": "{0};{1}".format(material.location.latitude, material.location.longitude),
            "factoryLocation": "{0};{1}".format(FACTORY_LOCATION[0], FACTORY_LOCATION[1]),
            "weight": material.weight,
            "material": material.name
        }
        payload["production"].append(value)
    
    response = requests.post(url, json=payload, headers=headers)

    data = response.json()
    production = data['productionCO2']
    
    return production
