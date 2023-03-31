import datetime

from miniching.hexagrams import Hexagram
from miniching.reading.models import HexagramText, Reading, LineText
from miniching.serialization import REFERENCE


def compose_reading(hexagram: Hexagram, timestamp: datetime.datetime, query: str, classic: bool) -> Reading:
    # for hexagrams with no changing lines, just return the origin hexagram text
    origin_text = HexagramText(REFERENCE[hexagram.origin]["title"], REFERENCE[hexagram.origin]["intro"],
                               REFERENCE[hexagram.origin]["judgement"], REFERENCE[hexagram.origin]["commentary"],
                               REFERENCE[hexagram.origin]["image"], REFERENCE[hexagram.origin]["image_commentary"])
    if not hexagram.trans:
        return Reading(timestamp, query, hexagram, origin_text, trans_text=None, lines_to_read=None)

    lines_to_read = []
    lines_apply_to_trans = False
    # special line comment edge case (hexagrams 1 and 2 with all 6 changing lines)
    if (hexagram.origin == '1' or hexagram.trans == '1') and len(hexagram.changing_lines) == 6:
        lines_to_read = [LineText("special", REFERENCE[hexagram.origin]["lines"]["special"]["text"],
                                  REFERENCE[hexagram.origin]["lines"]["special"]["comment"])]
        origin_text.lines = lines_to_read
    # Read core text only with 6 changing lines
    elif not classic and len(hexagram.changing_lines) == 6:
        pass
    # get lower, unchanging line when 4 or 5 changing lines
    elif not classic and len(hexagram.changing_lines) > 3:
        lines_apply_to_trans = True
        line_to_read = [str(line) for line in range(1, 7) if line not in hexagram.changing_lines][0]
        lines_to_read.append(LineText(line_to_read, REFERENCE[hexagram.trans]['lines'][line_to_read]["text"],
                                      REFERENCE[hexagram.trans]['lines'][line_to_read]["text"]))
    else:
        for line in hexagram.changing_lines:
            lines_to_read.append(LineText(line, REFERENCE[hexagram.origin]['lines'][line]["text"],
                                          REFERENCE[hexagram.origin]['lines'][line]["text"]))

    trans_text = HexagramText(REFERENCE[hexagram.trans]["title"], REFERENCE[hexagram.trans]["intro"],
                              REFERENCE[hexagram.trans]["judgement"], REFERENCE[hexagram.trans]["commentary"],
                              REFERENCE[hexagram.trans]["image"], REFERENCE[hexagram.trans]["image_commentary"])
    return Reading(timestamp, query, hexagram, origin_text, trans_text, lines_to_read, lines_apply_to_trans)
