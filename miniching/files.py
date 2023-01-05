import os
import json
from configparser import ConfigParser
import yaml

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

_config = ConfigParser()
with open(ROOT_DIR + "/config.ini", "r") as f:
    _config.read(f)


def get_config():
    return _config


def read_serialization_data(path) -> dict:
    with open(path, "r") as f:
        if ".json" in path:
            return json.load(f)
        elif ".yaml" in path:
            return yaml.safe_load(f)
    raise Exception("unsupported file format. specify files with .json or .yaml extensions")


def write_simple_history():
    pass


def write_map_history():
    pass


RESOURCES_PATH = ROOT_DIR + "/resources/"
REFERENCE = read_serialization_data(RESOURCES_PATH + "reference.yaml")
MODIFIED_ZHU_XI_LINE_EVALUATION = read_serialization_data(RESOURCES_PATH + "modified_zhu_xi_line_evaluation.yaml")
BINARY_TO_DECIMAL = read_serialization_data(RESOURCES_PATH + "binary_to_decimal.yaml")
DECIMAL_TO_BINARY = {value: key for key, value in BINARY_TO_DECIMAL.items()}
