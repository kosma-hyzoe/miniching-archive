import os
import yaml

from miniching import config


def read_yaml(path) -> dict:
    with open(path, "r") as f:
        return yaml.safe_load(f)


def write_history(parsed_reading: str):
    path_dir = config.HISTORY_DIR
    if path_dir == "default" or not path_dir:
        path = os.path.join(_DEFAULT_HISTORY_DIR, "iching-history.txt")
    else:
        path = os.path.join(path_dir, "iching-history.txt")

    with open(path, "a+") as f:
        f.write(parsed_reading)


_ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
_RESOURCES_DIR = os.path.join(_ROOT_DIR, "resources")
_DEFAULT_HISTORY_DIR = os.environ['HOME']

REFERENCE = read_yaml(os.path.join(_RESOURCES_DIR, "iching_reference.yaml"))
BINARY_TO_DECIMAL = read_yaml(os.path.join(_RESOURCES_DIR, "binary_to_decimal.yaml"))
DECIMAL_TO_BINARY = {value: key for key, value in BINARY_TO_DECIMAL.items()}
