import re
from random import choice
from typing import NamedTuple, Optional

from miniching.reference import DECIMAL_TO_BINARY, BINARY_TO_DECIMAL

VALUE_ERROR_MSG = "Invalid excerpt format. use '64' for pure hexagrams" \
                  " or '64:1,2,3' for hexagrams with changing lines." \
                  " Alternatively, use '3 coin sum' notation  - i.e. '788688'" \
                  " is the equivalent of '52:3'"


class Hexagram(NamedTuple):
    origin: str
    trans: Optional[str]
    chanlines: list[str]
    classic_eval: bool

    # effectively returns a miniching notation excerpt
    def __str__(self):
        if self.chanlines:
            return f"{self.origin}:{','.join(self.chanlines)}"
        else:
            return self.origin


def get_with_coin_toss(classic_eval: bool) -> Hexagram:
    chanlines: list[str] = []
    origin_binary: list[str] = []
    trans_binary: list[str] = []

    # Six 3-coin tosses are emulated. 0/1s are added to the hexagrams' binary
    # representation.  Note that in '000111'(11: "Peace"), the first character
    # corresponds to line 6 and last character to line 1 – I don't like it, but
    # this seems to be a common convention among I-Ching apps. The numbers of
    # changing lines are appended along the way.
    for line in range(1, 7):
        coin_sum = choice([2, 3]) + choice([2, 3]) + choice([2, 3])
        if coin_sum == 7:
            origin_binary.insert(0, "1")
            trans_binary.insert(0, "1")
        elif coin_sum == 8:
            origin_binary.insert(0, "0")
            trans_binary.insert(0, "0")
        elif coin_sum == 9:
            origin_binary.insert(0, "1")
            trans_binary.insert(0, "0")
            chanlines.append(str(line))
        elif coin_sum == 6:
            origin_binary.insert(0, "0")
            trans_binary.insert(0, "1")
            chanlines.append(str(line))

    origin_decimal = BINARY_TO_DECIMAL["".join(origin_binary)]
    trans_decimal = BINARY_TO_DECIMAL["".join(trans_binary)]
    return Hexagram(origin_decimal, trans_decimal, chanlines, classic_eval)


def get_from_excerpt(excerpt: str, classic_eval: bool) -> Hexagram:
    # for excerpts with no changing lines, in miniching notation
    if re.match(r"^\d{1,2}$", excerpt):
        origin = excerpt
        trans = None
        chanlines = []
    # for excerpts with changing lines, in miniching notation
    elif re.match(r"^\d{1,2}:(\d,){0,5}\d$", excerpt):
        origin = excerpt[: excerpt.index(":")]
        chanlines = excerpt[excerpt.index(":") + 1:].split(",")
        origin_binary = [value for value in DECIMAL_TO_BINARY[origin]]
        trans_binary = []
        zip_lines = zip([str(line) for line in range(6, 0, -1)], origin_binary)

        for line, line_value in zip_lines:
            opposite_line_value = "1" if line_value == "0" else "0"
            if line in chanlines:
                trans_binary.append(opposite_line_value)
            else:
                trans_binary.append(line_value)
        trans = BINARY_TO_DECIMAL["".join(trans_binary)]
    # excerpts in 'coin sum' notation, i.e. 788688 is the equivalent of 52:3
    elif re.match(r"^[6789]{6}$", excerpt):
        origin_binary = []
        trans_binary = []
        chanlines = []
        tmp_lines = [str(line) for line in range(6, 0, -1)]
        for coin_sum, line_number in zip(excerpt, tmp_lines):
            if coin_sum == "7":
                origin_binary.append("1")
                trans_binary.append("1")
            elif coin_sum == "8":
                origin_binary.append("0")
                trans_binary.append("0")
            elif coin_sum == "9":
                origin_binary.append("1")
                trans_binary.append("0")
                chanlines.append(line_number)
            elif coin_sum == "6":
                origin_binary.append("0")
                trans_binary.append("1")
                chanlines.append(line_number)

        origin = BINARY_TO_DECIMAL["".join(origin_binary)]
        trans = BINARY_TO_DECIMAL["".join(trans_binary)]
    else:
        raise ValueError(VALUE_ERROR_MSG)
    return Hexagram(origin, trans, chanlines, classic_eval)
