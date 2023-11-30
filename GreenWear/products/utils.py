import requests


FACTORY_LOCATION = ['43.6342', '11.5318']
SHIPPING_TO_LOCATION = ['43.5676', '11.5299']

'''
API REQUEST:
-----------------------------------------------------------------------------------
Suppose that we ship our merch directly from the factory,we just need to define 
the shipping location (when the user will buy our merch) and the materials location
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
            "shippingTo": "{0};{1}".format(SHIPPING_TO_LOCATION[0], SHIPPING_TO_LOCATION[1])
        },
        "production": []
    }
    
    for material in materials:
        value = {
            "materialLocation": "{0};{1}".format(material.latitude, material.longitude),
            "factoryLocation": "{0};{1}".format(FACTORY_LOCATION[0], FACTORY_LOCATION[1]),
            "weight": material.weight,
            "material": material.name
        }
        payload["production"].append(value)
    
    response = requests.post(url, json=payload, headers=headers)

    data = response.json()
    total = data['totalCO2']
    
    return total
