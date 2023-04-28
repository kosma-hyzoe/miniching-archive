from miniching import config
from miniching.serialization import REFERENCE


def get_result(hexagram):
    if not hexagram.trans:
        result = f"{hexagram.origin}"
    else:
        result = f"{hexagram.origin}:{','.join(hexagram.changing_lines)} -> {hexagram.trans}"

    return result


def get_unicode_hexagram_result(hexagram):
    origin_sign = REFERENCE[hexagram.origin]['sign']
    if not hexagram.trans:
        return origin_sign
    else:
        trans_sign = REFERENCE[hexagram.origin]['sign']
        return f"{origin_sign} -> {trans_sign}"


def format_datetime(datetime):
    return datetime.strftime(config.TIMESTAMP_FORMAT)


def format_hexagram_header(header):
    if "(" in header:
        header = header[:header.index("(") - 1]
    elif "[" in header:
        header = header[:header.index("[") - 1]
    return header
