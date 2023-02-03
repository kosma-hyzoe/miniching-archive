import re
from collections import OrderedDict

from miniching.files import DECIMAL_TO_BINARY, BINARY_TO_DECIMAL


def get_decoded_excerpt(excerpt: str) -> dict:
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
