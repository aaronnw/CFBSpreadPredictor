import os
import json


def file_access(path):
    return os.path.isfile(path) and os.access(path, os.R_OK)


def save_json(json_data, filepath):
    with open(filepath, 'w') as f:
        json.dump(json_data, f)


def load_json(filepath):
    with open(filepath) as file:
        return json.load(file)


def year_from_date(date):
    return str(date.split('-')[0])