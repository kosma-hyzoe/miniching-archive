from miniching.serialization import get_config, REFERENCE

try:
    _formats = dict(get_config().items("formats"))

    WIDTH = _formats["width"]
    LINE_BREAK = _formats["line_break"]
    SECTION_BREAK = _formats["section_break"]
    INITIAL_INDENT = _formats["initial_indent"]
    INDENT = _formats["indent"]
except:
    WIDTH = 80
    LINE_BREAK = "\n"
    SECTION_BREAK = LINE_BREAK * 2
    INITIAL_INDENT = ""
    INDENT = 2 * " "


def format_datetime(datetime):
    return datetime.strftime(_formats["timestamp"])


def format_result(result):
    hex_decimal = result[0]
    hex_sign = REFERENCE[hex_decimal]['sign']
    if len(result) == 1:
        result = f"{hex_decimal}"
        if get_config()["formats"].getboolean("unicode_result_mirroring"):
            result += f" : {hex_sign}"
    else:
        transformed_hex_decimal = result[1]
        transformed_hex_sign = REFERENCE[transformed_hex_decimal]['sign']
        result = f"{hex_decimal} -> {transformed_hex_decimal}"
        if get_config()["formats"].getboolean("unicode_result_mirroring"):
            result += f" : {hex_sign} -> {transformed_hex_sign}"

    return result


def format_hexagram_header(header):
    if "(" in header:
        header = header[:header.index("(") - 1]
    elif "[" in header:
        header = header[:header.index("[") - 1]

    return header
