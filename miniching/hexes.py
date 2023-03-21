import re
import random
from typing import NamedTuple, Optional

from miniching.serialization import DECIMAL_TO_BINARY, BINARY_TO_DECIMAL


class Hexagram(NamedTuple):
    origin_hexagram: str
    trans_hexagram: Optional[str]
    changing_lines: Optional[list[str]]

    def __str__(self):
        if self.changing_lines:
            changing_lines_representation = ",".join(self.changing_lines)
            return f"{self.origin_hexagram}:{changing_lines_representation}"
        else:
            return self.origin_hexagram


def get_hexagram_with_coin_toss() -> Hexagram:
    changing_lines: list[str] = []
    hex_binary: list[str] = []
    transformed_hex_binary: list[str] = []

    # Six 3-coin tosses are emulated. 0/1s are added to the hexagram binary representation.
    # Note that in "000111", first character corresponds to line 6 and last character to line 1 –
    # I don't like it, but this seems to be a common convention in I-Ching apps.
    # The numbers of changing lines are appended along the way.
    for line in range(1, 7):
        coin_sum = random.choice([2, 3]) + random.choice([2, 3]) + random.choice([2, 3])
        if coin_sum == 7:
            hex_binary.insert(0, '1')
            transformed_hex_binary.insert(0, '1')
        elif coin_sum == 8:
            hex_binary.insert(0, '0')
            transformed_hex_binary.insert(0, '0')
        elif coin_sum == 9:
            hex_binary.insert(0, '1')
            transformed_hex_binary.insert(0, '0')
            changing_lines.append(str(line))
        elif coin_sum == 6:
            hex_binary.insert(0, '0')
            transformed_hex_binary.insert(0, '1')
            changing_lines.append(str(line))

    hex_decimal = BINARY_TO_DECIMAL["".join(hex_binary)]
    transformed_hex_decimal = BINARY_TO_DECIMAL["".join(transformed_hex_binary)]

    return Hexagram(origin_hexagram=hex_decimal, trans_hexagram=transformed_hex_decimal, changing_lines=changing_lines)


def get_hexagram_from_excerpt(excerpt: str) -> Hexagram:
    # for excerpts with no changing lines, in miniching notation
    if re.match(r"\d{1,2}:(\d,){0,5}\d", excerpt):
        hex_decimal = excerpt
        hex_binary = DECIMAL_TO_BINARY[hex_decimal]
        changing_lines = None
        transformed_hex_decimal = None
    # for excerpts with changing lines, in miniching notation
    elif re.match(r"\d{1,2}", excerpt):
        hex_decimal = excerpt[:excerpt.index(":")]
        changing_lines = excerpt[excerpt.index(":") + 1:].split(",")
        hex_binary = [value for value in DECIMAL_TO_BINARY[hex_decimal]]
        transformed_hex_binary = []
        # todo probably can be simplified
        for position, line_value in zip(range(6, 0, -1), hex_binary):
            opposite_line_value = 1 if line_value == 0 else 0
            if position in changing_lines:
                transformed_hex_binary.append(opposite_line_value)
            else:
                transformed_hex_binary.append(line_value)
        transformed_hex_binary_representation = "".join(str(line) for line in transformed_hex_binary)
        transformed_hex_decimal = BINARY_TO_DECIMAL[transformed_hex_binary_representation]
    # excerpts in 'coin sum' notation, i.e.
    elif re.match(r"[6789]{6}", excerpt):
        hex_binary = []
        transformed_hex_binary = []
        changing_lines = []
        for coin_sum, line_number in zip(excerpt, range(6, 1, -1)):
            if coin_sum == 7:
                hex_binary.append('1')
                transformed_hex_binary.append('0')
            elif coin_sum == 8:
                hex_binary.append('0')
                transformed_hex_binary.append('0')
            elif coin_sum == 9:
                hex_binary.append('1')
                transformed_hex_binary.append('0')
                changing_lines.append(str(line_number))
            elif coin_sum == 6:
                hex_binary.append('0')
                transformed_hex_binary.append('1')
                changing_lines.append(str(line_number))

        hex_decimal = BINARY_TO_DECIMAL[hex_binary]
        transformed_hex_decimal = BINARY_TO_DECIMAL[transformed_hex_binary]
    else:
        raise ValueError("Invalid excerpt format. use '64' for pure hexagrams"
                         " or '64:1,2,3' for hexagrams with changing lines."
                         " Alternatively, use '3 coin sum' notation  – i.e. '788688' is the equivalent of '52:3'")

    return Hexagram(origin_hexagram=hex_decimal, trans_hexagram=transformed_hex_decimal, changing_lines=changing_lines)


