import os
import yaml


def _read_yaml(path):
    with open(path, "r") as f:
        return yaml.safe_load(f)


_ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
_RESOURCES_DIR = os.path.join(_ROOT_DIR, "resources")

REFERENCE = _read_yaml(os.path.join(_RESOURCES_DIR, "iching_reference.yaml"))
BINARY_TO_DECIMAL = _read_yaml(os.path.join(_RESOURCES_DIR, "bin_to_dec.yaml"))
DECIMAL_TO_BINARY = {value: key for key, value in BINARY_TO_DECIMAL.items()}
