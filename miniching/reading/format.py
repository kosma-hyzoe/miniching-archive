from miniching import config
from miniching.serialization import REFERENCE


def get_result(hexagram):
    origin_sign = REFERENCE[hexagram.origin]['sign']
    if not hexagram.trans:
        result = f"{hexagram.origin}"
        if config.UNICODE_HEXAGRAM_MIRROR:
            result += f" | {origin_sign}"
    else:
        trans_sign = REFERENCE[hexagram.origin]['sign']
        result = f"{hexagram.origin}:{','.join(hexagram.changing_lines)} -> {hexagram.trans}"
        if config.UNICODE_HEXAGRAM_MIRROR:
            result += f" | {origin_sign} -> {trans_sign}"

    return result


def format_datetime(datetime):
    return datetime.strftime(config.TIMESTAMP_FORMAT)


def format_hexagram_header(header):
    if "(" in header:
        header = header[:header.index("(") - 1]
    elif "[" in header:
        header = header[:header.index("[") - 1]
    return header
