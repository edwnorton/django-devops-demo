import os
import yaml


def get_yaml_data(yaml_file_path):
    yaml_file = os.path.join(yaml_file_path, 'conf.yaml')
    with open(yaml_file, 'r', encoding="utf-8") as f:
        file_data = f.read()
    data = yaml.full_load(file_data)
    return data


