import json
import os


DATA_FILE_NAME = 'data.json'
DATA_FILE_NAME = os.path.join(os.path.dirname(__file__), DATA_FILE_NAME)


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


def save_profile_data(category, profile_id, data):
    with open(DATA_FILE_NAME, 'r') as file:
        all_data = json.load(file)
    if category not in all_data:
        all_data[category] = {}
    all_data[category][profile_id] = data
    with open(DATA_FILE_NAME, 'w') as file:
        json.dump(all_data, file)


def load_profile_data(category, profile_id):
    if not os.path.exists(DATA_FILE_NAME):
        return {}
    try:
        with open(DATA_FILE_NAME, 'r') as file:
            all_data = json.load(file)
        return all_data.get(category, {}).get(profile_id, None)
    except json.JSONDecodeError:
        return {}
