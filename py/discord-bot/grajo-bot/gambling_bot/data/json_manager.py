import json
import os

DATA_FILE_NAME = os.path.join(os.path.dirname(__file__), 'data.json')
# categories: players, dealers, tables

def load_data(*path):
    if not os.path.exists(DATA_FILE_NAME):
        return {}
    try:
        with open(DATA_FILE_NAME, 'r') as file:
            all_data = json.load(file)
        # traverse the path to reach the desired subcategory
        for key in path:
            all_data = all_data.get(key, {})
        return all_data
    except json.JSONDecodeError:
        return {}


def save_data(data, *path):
    if not os.path.exists(DATA_FILE_NAME):
        all_data = {}
    else:
        with open(DATA_FILE_NAME, 'r') as file:
            try:
                all_data = json.load(file)
            except json.JSONDecodeError:
                all_data = {}

    # create nested dictionaries as needed and assign data
    d = all_data
    for key in path[:-1]:
        d = d.setdefault(key, {})
    d[path[-1]] = data

    with open(DATA_FILE_NAME, 'w') as file:
        json.dump(all_data, file, indent=4)


def delete_data(*path):
    if not os.path.exists(DATA_FILE_NAME):
        return
    try:
        with open(DATA_FILE_NAME, 'r') as file:
            all_data = json.load(file)
    except json.JSONDecodeError:
        return

    # traverse to the last nested dictionary
    d = all_data
    for key in path[:-1]:
        d = d.get(key)
        if d is None:
            return  # path does not exist, nothing to delete

    # delete the last key in the path
    d.pop(path[-1], None)

    # save the modified data back to the file
    with open(DATA_FILE_NAME, 'w') as file:
        json.dump(all_data, file, indent=4)
