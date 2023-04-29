import sys
from datetime import datetime
import config
from miniching.hexagrams import Hexagram
from miniching.reference import REFERENCE


def get_result(hexagram: Hexagram):
    result = f"{hexagram.origin}"

    if not hexagram.classic_eval and len(hexagram.chanlines) in [4, 5]:
        return result + f" -> {hexagram.trans}:{','.join(hexagram.chanlines)}"
    elif hexagram.chanlines:
        return result + f":{','.join(hexagram.chanlines)} -> {hexagram.trans}"
    else:
        return result


def get_unicode_hexagram_result(hexagram):
    origin_sign = REFERENCE[hexagram.origin]['sign']
    if not hexagram.trans:
        return origin_sign
    else:
        trans_sign = REFERENCE[hexagram.origin]['sign']
        return f"{origin_sign} -> {trans_sign}"


def format_timestamp(timestamp):
    try:
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
