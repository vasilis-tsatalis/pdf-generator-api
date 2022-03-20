import json

async def read_bindings(criteria, value, filename='properties/bindings.json'):
    """
    Criteria parameter should be code or name keys
    """
    # Opening JSON file
    f = open(filename)
    # returns JSON object as a dictionary
    data = json.load(f)

    # Iterating through the json list
    for item in data['documents']:
        if item[criteria] == value:
            status = True
            break
        else:
            status = False
    return status

async def read_templates_details(filename='properties/bindings.json'):
    # Opening JSON file
    f = open(filename)
    # returns JSON object as a dictionary
    data = json.load(f)
    templates = data['documents']
    return templates


def read_configuration(key: str, filename='properties/config.json'):
    # Opening JSON file
    configuration_file = open(filename)
    # returns JSON object as a dictionary
    parameters = json.load(configuration_file)
    # Close file
    configuration_file.close()
    # Load values
    value = str(parameters['system_parameters'][key])
    return value
