import json
from decouple import config
 
# function to add to JSON - bindings
async def write_json_bindings(new_data, filename=f"{config('BINDINGS_FILE')}"):

    with open(filename,'a') as file:
        # load existing data into a dict.
        file_data = json.load(file)
        # Join new_data with file_data inside emp_details
        file_data["documents"].append(new_data)
        # Sets file's current position at offset.
        file.seek(0)
        # convert back to json.
        json.dump(file_data, file, indent = 4)
