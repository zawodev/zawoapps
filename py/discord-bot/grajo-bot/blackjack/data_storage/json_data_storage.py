import json
import os


DATA_FILE_NAME = 'data.json'


def save_data(category, data):
    with open(DATA_FILE_NAME, 'r') as file:
        all_data = json.load(file)
    all_data[category] = data
    with open(DATA_FILE_NAME, 'w') as file:
        json.dump(all_data, file)


def load_data(category):
    if not os.path.exists(DATA_FILE_NAME):
        return {}
    try:
        with open(DATA_FILE_NAME, 'r') as file:
            all_data = json.load(file)
        return all_data.get(category, None)
    except json.JSONDecodeError:
        return {}

