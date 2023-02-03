from collections import OrderedDict

from miniching.excerpt import get_decoded_excerpt
from miniching.files import REFERENCE, MODIFIED_ZHU_XI_LINE_EVALUATION


def compose_reading(excerpt: str, timestamp: str, query: str, classic: bool) -> dict:
    decoded_excerpt = get_decoded_excerpt(excerpt)
    reading = OrderedDict({"timestamp": timestamp, "query": query})

    hex_decimal = decoded_excerpt["hex_decimal"]
    changing_lines = decoded_excerpt["changing_lines"]

    hexagram_dict = {
        "title": REFERENCE[hex_decimal]["title"],
        "intro": REFERENCE[hex_decimal]["intro"],
        "judgement": REFERENCE[hex_decimal]["judgement"],
        "commentary": REFERENCE[hex_decimal]["commentary"],
        "image": REFERENCE[hex_decimal]["image"],
        "image_commentary": REFERENCE[hex_decimal]["image_commentary"],
    }

    if not changing_lines:
        reading['result'] = tuple([hex_decimal])
        reading["hexagram"] = hexagram_dict
        return reading

    transformed_hex_decimal = decoded_excerpt["transformed_hex_decimal"]
    reading['result'] = tuple([hex_decimal, transformed_hex_decimal])

    reading["changing_lines"] = ", ".join([str(line) for line in changing_lines])
    if not classic:
        reading["lines_to_read"] = MODIFIED_ZHU_XI_LINE_EVALUATION[len(changing_lines)]

    reading["hexagram"] = hexagram_dict
    reading["transformed_hexagram"] = {
        "title": REFERENCE[transformed_hex_decimal]["title"],
        "intro": REFERENCE[transformed_hex_decimal]["intro"],
        "judgement": REFERENCE[transformed_hex_decimal]["judgement"],
        "commentary": REFERENCE[transformed_hex_decimal]["commentary"],
        "image": REFERENCE[transformed_hex_decimal]["image"],
        "image_commentary": REFERENCE[transformed_hex_decimal]["image_commentary"],
    }

    if len(changing_lines) == 6 and hex_decimal == 1 or len(changing_lines) == 6 and hex_decimal == 2:
        reading["hexagram"]["lines"] = {}
        reading["hexagram"]["lines"]["special_comment"] = REFERENCE[hex_decimal]["lines"]["special"]
    elif not classic and len(changing_lines) == 4 or not classic and len(changing_lines) == 5:
        line_to_read = [line for line in range(1, 7) if line not in changing_lines][0]
        reading["transformed_hexagram"]["lines"] = {}
        line_to_read = REFERENCE[transformed_hex_decimal]["lines"][line_to_read]
        reading["transformed_hexagram"]["lines"][line_to_read] = line_to_read

    lines_reference = REFERENCE[hex_decimal]["lines"]
    reading["hexagram"]["lines"] = {}
    [reading["hexagram"]["lines"].update({line: lines_reference[line]}) for line in changing_lines]

    return reading
