import datetime
from miniching.hexagrams import Hexagram

from miniching.reading.models import HexagramText, Reading, LineText
from miniching.reference import REFERENCE


def compose(hexagram: Hexagram, timestamp, query):
    # for hexagrams with no changing lines, just return the origin hexagram text
    origin_t = HexagramText(
        REFERENCE[hexagram.origin]["title"],
        REFERENCE[hexagram.origin]["intro"],
        REFERENCE[hexagram.origin]["judgement"],
        REFERENCE[hexagram.origin]["commentary"],
        REFERENCE[hexagram.origin]["image"],
        REFERENCE[hexagram.origin]["image_commentary"],
    )
    if not hexagram.trans:
        return Reading(timestamp, query, hexagram, origin_t, None, [], False)

    lines_to_read = []
    # special line comment edge case (hexagrams 1 and 2 with all 6 changing lines)
    if hexagram.origin in ["1", "2"] and len(hexagram.chanlines) == 6: # type: ignore
        lines_to_read = [LineText("special",
                                  REFERENCE[hexagram.origin]["lines"]["special"]["text"],
                                  REFERENCE[hexagram.origin]["lines"]["special"]["comment"],
                                  )
                         ]
        origin_t.lines = lines_to_read
    # Read core text only with 6 changing lines
    elif not hexagram.classic_eval and len(hexagram.chanlines) == 6: # type: ignore
        pass
    # get lower, unchanging line when 4 or 5 changing lines
    elif not hexagram.classic_eval and len(hexagram.chanlines) > 3:
        l = [str(l) for l in range(1, 7) if str(
            l) not in hexagram.chanlines][0]
        trans_lines = True
        lines_to_read.append(LineText(l, REFERENCE[hexagram.trans]["lines"][l]["text"],
                                      REFERENCE[hexagram.trans]["lines"][l]["text"],
                                      )
                             )
    else:
        for line in hexagram.chanlines:
            lines_to_read.append(
                LineText(
                    line,
                    REFERENCE[hexagram.origin]["lines"][line]["text"],
                    REFERENCE[hexagram.origin]["lines"][line]["text"],
                )
            )

    trans_text = HexagramText(
        REFERENCE[hexagram.trans]["title"],
        REFERENCE[hexagram.trans]["intro"],
        REFERENCE[hexagram.trans]["judgement"],
        REFERENCE[hexagram.trans]["commentary"],
        REFERENCE[hexagram.trans]["image"],
        REFERENCE[hexagram.trans]["image_commentary"],
    )
    return Reading(
        timestamp,
        query,
        hexagram,
        origin_t,
        trans_text,
        lines_to_read,
        trans_lines,
    )
