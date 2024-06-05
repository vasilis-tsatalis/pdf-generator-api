import json
from decouple import config

async def read_bindings(criteria, value, filename=f"{config('BINDINGS_FILE')}"):
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

async def read_templates_details(filename=f"{config('BINDINGS_FILE')}"):
    # Opening JSON file
    f = open(filename)
    # returns JSON object as a dictionary
    data = json.load(f)
    templates = data['documents']
    return templates

async def read_authenticated_users(filename=f"{config('AUTH_CONFIG_FILE')}"):
    # Opening JSON file
    f = open(filename)
    # returns JSON object as a dictionary
    data = json.load(f)
    auth_users = data['api_users']
    return auth_users
