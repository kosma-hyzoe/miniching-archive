import sys
from datetime import datetime
from miniching import config
from miniching.hexagrams import Hexagram
from miniching.reference import REFERENCE


def get_result(hexagram: Hexagram):
    result = f"{hexagram.origin}"

    if hexagram.lines:
        if not hexagram.classic_eval and len(hexagram.lines) in [4, 5]:
            result += f" -> {hexagram.trans}:{','.join(hexagram.lines)}"
        else:
            result += f":{','.join(hexagram.lines)} -> {hexagram.trans}"
        if config.HEX_MIRROR:
            result += f" : {REFERENCE[hexagram.origin]['sign']}" \
                      f" -> {REFERENCE[hexagram.trans]['sign']}"
    else:
        if config.HEX_MIRROR:
            result += f" : {REFERENCE[hexagram.origin]['sign']}"
    return result


def format_timestamp(timestamp):
    try:
        datetime.strptime(str(timestamp), config.TIMESTAMP_FORMAT)
    except ValueError as e:
        print("Error: " + str(e) + " provided in the config file.")
        sys.exit(1)
    return timestamp.strftime(config.TIMESTAMP_FORMAT)


def format_hexagram_title(title):
    if "(" in title:
        title = title[:title.index("(") - 1]
    elif "[" in title:
        title = title[:title.index("[") - 1]
    return title
