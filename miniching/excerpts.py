import random
import re
from collections import OrderedDict

from miniching.files import BINARY_TO_DECIMAL, DECIMAL_TO_BINARY


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


def get_decoded_excerpt(excerpt: str):
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



