import random
from miniching.serialization import BINARY_TO_DECIMAL


def get_excerpt_with_coin_toss() -> str:
    changing_lines: list[str] = []
    hex_binary: list[str] = []

    # Six 3-coin tosses are emulated. 0/1s are added to the hexagram binary representation.
    # Note that in "000111", first character corresponds to line 6 and last character to line 1 –
    # I don't like it, but this seems to be a common convention in I-Ching apps.
    # The numbers of changing lines are appended along the way.
    for line in range(1, 7):
        coin_throw_sum = random.choice([2, 3]) + random.choice([2, 3]) + random.choice([2, 3])
        hex_binary.insert(0, '0') if coin_throw_sum % 2 == 0 else hex_binary.insert(0, '1')
        if coin_throw_sum == 6 or coin_throw_sum == 9:
            changing_lines.append(str(line))

    hex_decimal = BINARY_TO_DECIMAL["".join(hex_binary)]
    if changing_lines:
        changing_lines_representation = ",".join(changing_lines)
        return f"{hex_decimal}:{changing_lines_representation}"
    else:
        return str(hex_decimal)




