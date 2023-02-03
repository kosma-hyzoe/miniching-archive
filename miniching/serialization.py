import os
from configparser import ConfigParser
import yaml

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

_config = ConfigParser()
_config.read_file(open(ROOT_DIR + "/config.ini"))


def get_config():
    return _config


def read(path) -> dict:
    with open(path, "r") as f:
        return yaml.safe_load(f)


def write_history(parsed_reading: str):
    path_dir = get_config().get("paths", "simple_history_dir")
    if path_dir == "default":
        path = os.path.join(_DEFAULT_HISTORY_DIR, "iching-history.txt")
    else:
        path = os.path.join(path_dir, "iching-history.txt")

    with open(path, "a+") as f:
        f.write(parsed_reading)


_RESOURCES_DIR = os.path.join(ROOT_DIR, "resources")
_DEFAULT_HISTORY_DIR = os.environ['HOME']

REFERENCE = read(_RESOURCES_DIR + "/iching_reference.yaml")
MODIFIED_ZHU_XI_LINE_EVALUATION = read(_RESOURCES_DIR + "/modified_zhu_xi_line_evaluation.yaml")
BINARY_TO_DECIMAL = read(_RESOURCES_DIR + "/binary_to_decimal.yaml")
DECIMAL_TO_BINARY = {value: key for key, value in BINARY_TO_DECIMAL.items()}
