import argparse
from datetime import datetime
from collections import OrderedDict
from pprint import pprint
from textwrap import wrap

from miniching.files import BINARY_TO_DECIMAL, DECIMAL_TO_BINARY, write_simple_history, write_map_history, \
    MODIFIED_ZHU_XI_LINE_EVALUATION, \
    REFERENCE
import random
import re

from miniching.reading_parser import ReadingParser


def main():
    modes = _get_parser_args()

    now = datetime.now().isoformat(timespec="minutes")
    if modes.quick:
        query = "..."
        timestamp = now
        excerpt = get_excerpt_with_coin_toss()
    else:
        timestamp = input("Timestamp: ") if modes.evaluate_from_excerpt else now
        timestamp = now if timestamp == "now" else timestamp
        query = input("Query: ")
        excerpt = input("Excerpt: ") if modes.evaluate_from_excerpt else get_excerpt_with_coin_toss()

    # decoded_excerpt = decode_excerpt(excerpt)
    decoded_excerpt = decode_excerpt("2:1,4")

    reading = get_reading(timestamp, query, decoded_excerpt, modes.classic, modes.full_text)

    if not modes.no_print:
        reading_parser = ReadingParser(reading)
        print(reading_parser.get_parsed_reading(skip_query=True, skip_timestamp=True))

    if modes.simple_history:
        write_simple_history()
    if modes.map_history:
        write_map_history()


def _get_parser_args():
    parser = argparse.ArgumentParser()

    quick_help = "get reading with other args overriden to default, empty query and current timestamp"
    parser.add_argument('-q', '--quick', action="store_true", help=quick_help)
    classic_help = "use classic evaluation / 'read all changing lines' instead of default modified Zhu Xi method"
    parser.add_argument('-c', '--classic', action='store_true', help=classic_help)
    evaluate_help = "get reading from prompted excerpt using '64' format for pure hexes or '63:1,2' with changing lines"
    parser.add_argument('-e', '--evaluate-from-excerpt', action='store_true', help=evaluate_help)
    parser.add_argument('-f', '--full-text', action='store_true', help='get a full reading')
    parser.add_argument('-n', '--no-print', action='store_true', help='skip printing the reading')
    parser.add_argument('-s', '--simple-history', action='store_true', help='write to simple history file')
    parser.add_argument('-m', '--map-history', action='store_true', help='write to map history file')
    return parser.parse_args()


def get_excerpt_with_coin_toss() -> str:
    changing_lines = []
    reversed_hex_binary = []

    for line in range(1, 7):
        coin_throw_sum = random.choice([2, 3]) + random.choice([2, 3]) + random.choice([2, 3])
        reversed_hex_binary.append(0) if coin_throw_sum % 2 == 0 else reversed_hex_binary.append(1)
        if coin_throw_sum == 6 or coin_throw_sum == 9:
            changing_lines.append(line)

    hex_binary_representation = "".join(str(line) for line in reversed_hex_binary[::-1])
    hex_decimal = BINARY_TO_DECIMAL[hex_binary_representation]
    if changing_lines:
        changing_lines_representation = ",".join(str(line) for line in changing_lines)
        return f"{hex_decimal}:{changing_lines_representation}"
    else:
        return str(hex_decimal)


def decode_excerpt(excerpt: str):
    if not re.match(r"\d{1,2}:(\d,){0,5}\d", excerpt) and not re.match(r"\d{1,2}", excerpt):
        raise ValueError("invalid excerpt format. use '64' for pure hexes or '64:1,2,3' for hexes with changing lines")

    if ":" not in excerpt:
        hex_decimal = int(excerpt)
        changing_lines = None
    else:
        hex_decimal = int(excerpt[:excerpt.index(":")])
        changing_lines = excerpt[excerpt.index(":") + 1:].split(",")
        changing_lines = [int(line) for line in changing_lines]

    hex_binary = [int(value) for value in list(DECIMAL_TO_BINARY[hex_decimal])]
    transformed_hex_binary = []
    if changing_lines:
        for position, line_value in zip(range(6, 0, -1), hex_binary):
            opposite_line_value = 1 if line_value == 0 else 0
            if position in changing_lines:
                transformed_hex_binary.append(opposite_line_value)
            else:
                transformed_hex_binary.append(line_value)
        transformed_hex_binary_representation = "".join(str(line) for line in transformed_hex_binary)
        transformed_hex_decimal = BINARY_TO_DECIMAL[transformed_hex_binary_representation]
    else:
        transformed_hex_decimal = None

    decoded_excerpt = OrderedDict({
        "hex_decimal": hex_decimal,
        "hex_binary": hex_binary,
        "transformed_hex_decimal": transformed_hex_decimal,
        "transformed_hex_binary": transformed_hex_binary,
        "changing_lines": changing_lines
    })
    return decoded_excerpt


def get_reading(timestamp: str, query: str, decoded_excerpt: dict, classic=False, full_text=False) -> dict:
    hex_decimal = decoded_excerpt["hex_decimal"]
    transformed_hex_decimal = decoded_excerpt["transformed_hex_decimal"]
    changing_lines = decoded_excerpt["changing_lines"]

    reading = OrderedDict({"timestamp": timestamp, "query": query})

    hex_sign = REFERENCE[hex_decimal]['sign']
    if not transformed_hex_decimal:
        reading["result"] = f"{hex_decimal} : {hex_sign}"
    else:
        transformed_hex_sign = REFERENCE[transformed_hex_decimal]['sign']
        reading["result"] = f"{hex_decimal} -> {transformed_hex_decimal} : {hex_sign} -> {transformed_hex_sign}"

    if not full_text:
        if classic and changing_lines:
            reading["changing_lines"] = ", ".join([str(line) for line in changing_lines])
        elif changing_lines:
            reading["changing_lines"] = ", ".join([str(line) for line in changing_lines])
            reading["lines_to_read"] = MODIFIED_ZHU_XI_LINE_EVALUATION[len(changing_lines)]
        return reading

    hex_dictionary = {
        "title": REFERENCE[hex_decimal]["title"],
        "intro": REFERENCE[hex_decimal]["intro"],
        "judgement": REFERENCE[hex_decimal]["judgement"],
        "commentary": REFERENCE[hex_decimal]["commentary"],
        "image": REFERENCE[hex_decimal]["image"],
        "image_commentary": REFERENCE[hex_decimal]["image_commentary"],
    }
    if not transformed_hex_decimal:
        reading['hexagram'] = hex_dictionary
        return reading

    reading["hexagram"] = hex_dictionary
    reading["transformed_hexagram"] = {
        "title": REFERENCE[transformed_hex_decimal]["title"],
        "intro": REFERENCE[transformed_hex_decimal]["intro"],
        "judgement": REFERENCE[transformed_hex_decimal]["judgement"],
        "commentary": REFERENCE[transformed_hex_decimal]["commentary"],
        "image": REFERENCE[transformed_hex_decimal]["image"],
        "image_commentary": REFERENCE[transformed_hex_decimal]["image_commentary"],
    }
    if len(changing_lines) == 6 and hex_decimal == 1 or len(changing_lines) == 6 and hex_decimal == 2:
        reading["hexagram"]["special_comment"] = REFERENCE[hex_decimal]["lines"]["special"]
    elif not classic and len(changing_lines) == 4 or not classic and len(changing_lines) == 5:
        line_to_read = [line for line in range(1, 6 + 1) if line not in changing_lines][0]
        reading["transformed_hexagram"][line_to_read] = REFERENCE[transformed_hex_decimal]["lines"][line_to_read]
    else:
        lines_reference = REFERENCE[hex_decimal]["lines"]
        [reading["hexagram"].update({line: lines_reference[line]}) for line in changing_lines]
    return reading


if __name__ == "__main__":
    main()

