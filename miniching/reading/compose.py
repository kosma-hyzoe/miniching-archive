from miniching.hexagrams import Hexagram

from miniching.reading.models import HexagramText, Reading, LineText
from miniching.reference import REFERENCE


def compose(hexagram: Hexagram, timestamp, query):
    # for hexagrams with no changing lines, just return the origin hexagram text
    origin_text = _compose_hex_text(hexagram, trans=False)
    if not hexagram.trans:
        return Reading(timestamp, query, hexagram, origin_text, None, [])

    trans_lines = False
    lines_to_read = []

    # special line comment edge case (hexagrams 1, 2 with all 6 changing lines)
    if hexagram.origin in ["1", "2"] and len(hexagram.lines) == 6:
        _append_line_to_read(lines_to_read, hexagram, "s")
    # Read core text only with 6 changing lines
    elif not hexagram.classic_eval and len(hexagram.lines) == 6:
        pass
    # get lower, unchanging line when 4 or 5 changing lines
    elif not hexagram.classic_eval and len(hexagram.lines) > 3:
        line = [str(l) for l in range(1, 7) if str(l) not in hexagram.lines][0]
        trans_lines = True
        _append_line_to_read(lines_to_read, hexagram, line, trans_lines)
    else:
        for line in hexagram.lines:
            _append_line_to_read(lines_to_read, hexagram, line)

    trans_text = _compose_hex_text(hexagram, trans=True)
    return Reading(timestamp, query, hexagram, origin_text, trans_text,
                   lines_to_read, trans_lines)


def _append_line_to_read(lines_to_read, hexagram, line, trans_lines=False):
    if line == 's':
        text = REFERENCE[hexagram.origin]["lines"]["special"]["text"]
        comment = REFERENCE[hexagram.origin]["lines"]["special"]["comment"]
        lines_to_read.append(LineText("Special", text, comment))
    elif trans_lines:
        text = REFERENCE[hexagram.trans]["lines"][line]["text"]
        comment = REFERENCE[hexagram.trans]["lines"][line]["comment"]
        lines_to_read.append(LineText(line, text, comment))
    else:
        text = REFERENCE[hexagram.origin]["lines"][line]["text"]
        comment = REFERENCE[hexagram.origin]["lines"][line]["comment"]
        lines_to_read.append(LineText(line, text, comment))


def _compose_hex_text(hexagram, trans: bool):
    trans_or_origin = hexagram.trans if trans else hexagram.origin
    return HexagramText(
        REFERENCE[trans_or_origin]["title"],
        REFERENCE[trans_or_origin]["intro"],
        REFERENCE[trans_or_origin]["judgement"],
        REFERENCE[trans_or_origin]["commentary"],
        REFERENCE[trans_or_origin]["image"],
        REFERENCE[trans_or_origin]["image_commentary"],
    )
