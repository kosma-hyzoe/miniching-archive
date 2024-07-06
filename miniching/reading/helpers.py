import sys
from datetime import datetime
from miniching.hexagrams import Hexagram
from miniching.reference import REFERENCE


def get_result(hexagram: Hexagram,
               center: bool = True, hex_mirror: bool = False):
    result = f"{hexagram.origin}"

    if hexagram.lines:
        if not hexagram.classic_eval and len(hexagram.lines) in [4, 5]:
            l_to_read = get_line_to_read_4_or_5_changing_lines(hexagram.lines)
            result += f" -> {hexagram.trans}:{l_to_read}"
        else:
            result += f":{','.join(hexagram.lines)} -> {hexagram.trans}"

        if hex_mirror:
            result += f" : {REFERENCE[hexagram.origin]['sign']}" \
                      f" -> {REFERENCE[hexagram.trans]['sign']}"
    else:
        if hex_mirror:
            result += f" : {REFERENCE[hexagram.origin]['sign']}"

    return result.center(WIDTH) if center else result


def get_line_to_read_4_or_5_changing_lines(lines: list[str]):
    opposite_lines = [str(l) for l in range(1, 7) if str(l) not in lines]
    return opposite_lines[0]


def format_timestamp(timestamp):
    try:
        datetime.strptime(str(timestamp), rc.TIMESTAMP_FORMAT)
    except ValueError as e:
        print("Error: " + str(e) + " provided in the rc file.")
        sys.exit(1)
    return timestamp.strftime(rc.TIMESTAMP_FORMAT)


def format_hexagram_title(title):
    if "(" in title:
        title = title[:title.index("(") - 1]
    elif "[" in title:
        title = title[:title.index("[") - 1]
    return title
