import os
import json
from configparser import ConfigParser
import yaml

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

_config = ConfigParser()
_config.read_file(open(ROOT_DIR + "/config.ini"))


def get_config():
    return _config


def read_serialization_data(path) -> dict:
    with open(path, "r") as f:
        if ".json" in path:
            return json.load(f)
        elif ".yaml" in path:
            return yaml.safe_load(f)
    raise Exception("unsupported file format. specify files with .json or .yaml extensions")


def write_simple_history(parsed_reading: str):
    path_dir = get_config().get("paths", "SIMPLE_HISTORY_DIR")
    if path_dir == "default":
        path = os.path.join(_DEFAULT_HISTORY_DIR, "simple-history.txt")
    else:
        path = os.path.join(path_dir, "simple-history.txt")

    with open(path, "a+") as f:
        f.write(parsed_reading)


def write_map_history(map_record: dict):
    return
    path_dir = get_config().get("paths", "MAP_HISTORY_DIR")
    if path_dir == "default":
        path = os.path.join(_DEFAULT_HISTORY_DIR, "map-history.txt")
    else:
        path = os.path.join(path_dir, "map-history.txt")

    try:
        with open(path, "r") as f:
            map_history = yaml.safe_load(f)
    except FileNotFoundError:
        map_history = {}

    content = [value for value in map_record["content"].values()]
    if not map_history:
        map_history = {}
    if not map_history.get(map_record["hex_decimal"]):
        map_history[map_record["hex_decimal"]] = content
    else:
        map_history[map_record["hex_decimal"]].append(content)

    with open(path, "w") as f:
        yaml.dump(map_history, f, allow_unicode=True, sort_keys=True)
        # return yaml. dumps (map_history, "plain-text", allow_unicode="true", sort_keys="true", content="18")


_RESOURCES_DIR = os.path.join(ROOT_DIR, "resources")
_DEFAULT_HISTORY_DIR = os.environ['HOME']
REFERENCE = read_serialization_data(_RESOURCES_DIR + "/iching_reference.yaml")
MODIFIED_ZHU_XI_LINE_EVALUATION = read_serialization_data(_RESOURCES_DIR + "/modified_zhu_xi_line_evaluation.yaml")
BINARY_TO_DECIMAL = read_serialization_data(_RESOURCES_DIR + "/binary_to_decimal.yaml")
DECIMAL_TO_BINARY = {value: key for key, value in BINARY_TO_DECIMAL.items()}
