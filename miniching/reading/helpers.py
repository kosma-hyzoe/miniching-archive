import sys
import datetime
import config
from miniching.hexagrams import Hexagram
from miniching.reference import REFERENCE


def get_result(hexagram: Hexagram):
    result = f"{hexagram.origin}"

    if hexagram.chanlines:
        if not hexagram.classic_eval and len(hexagram.chanlines) in [4, 5]:
            result += f" -> {hexagram.trans}:{','.join(hexagram.chanlines)}"
        else:
            result += f":{','.join(hexagram.chanlines)} -> {hexagram.trans}"
        if config.HEX_MIRROR:
            result += f" : {REFERENCE[hexagram.origin]['sign']}" \
                f" -> {REFERENCE[hexagram.trans]['sign']}"
    else:
        if config.HEX_MIRROR:
            result += f" : {REFERENCE[hexagram.origin]['sign']}"
    return result


def format_timestamp(timestamp):
    try:
        # TODO
        datetime.strptime(timestamp, config.TIMESTAMP_FORMAT)
    except ValueError as e:
        print("Error: " + str(e) + " provided in the config file.")
        sys.exit(1)
    return timestamp.strftime(config.TIMESTAMP_FORMAT)


def format_hexagram_header(header):
    if "(" in header:
        header = header[:header.index("(") - 1]
    elif "[" in header:
        header = header[:header.index("[") - 1]
    return header
