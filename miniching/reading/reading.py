import os
from textwrap import wrap
from miniching.config import WIDTH, LINE_BREAK, SECTION_BREAK, INDENT
from miniching.config import HISTORY_PATH

from miniching.reading.helpers import get_result, format_hexagram_title
from miniching.reading.models import Reading, HexagramText, LineText

_DEFAULT_HISTORY_DIR = os.environ["HOME"]
HISTORY_FILENAME = "iching-history.txt"
_reading_sections = []


def write_history(reading: Reading):
    record = []

    record.extend([f"{str(reading.timestamp).center(WIDTH)}", LINE_BREAK])

    if len(reading.query) > WIDTH:
        record.append(LINE_BREAK.join(wrap(reading.query.center(WIDTH), WIDTH)))
    else:
        record.append(reading.query.center(WIDTH))

    record.append(get_result(reading.hexagram).center(WIDTH))

    if not HISTORY_PATH:
        path = os.path.join(_DEFAULT_HISTORY_DIR, HISTORY_FILENAME)
    elif not os.path.isfile(HISTORY_PATH):
        path = os.path.join(HISTORY_PATH, HISTORY_FILENAME)
    else:
        path = HISTORY_PATH

    with open(path, "a+") as f:
        f.write("\n".join(record) + "\n")


def get_printable_reading(reading: Reading) -> str:
    _reading_sections.extend([get_result(reading.hexagram), SECTION_BREAK])

    if reading.trans_text and reading.trans_lines:
        _parse_hexagram(reading.origin_text)
        _parse_hexagram(reading.trans_text, reading.lines_to_read)
    elif reading.trans_text:
        _parse_hexagram(reading.origin_text, reading.lines_to_read)
        _parse_hexagram(reading.trans_text)
    else:
        _parse_hexagram(reading.origin_text)
    return LINE_BREAK + "".join(_reading_sections)


def _parse_hexagram(text: HexagramText, lines_to_read: list[LineText] = None):
    _parse_header(format_hexagram_title(text.title), center=True)
    _parse_text(text.intro)

    _parse_text(text.judgement, preserve_line_breaks=True)
    _parse_text(text.commentary)

    _parse_text(text.image, preserve_line_breaks=True)
    _parse_text(text.image_commentary)

    if lines_to_read:
        for line in lines_to_read:
            if line.line == "Special":
                _parse_header("Special line comment:")
            else:
                _parse_header(f"Line {line.line}: ", indent=True)

            _parse_text(line.text, preserve_line_breaks=True)
            _parse_text(line.comment)


def _parse_header(header, center=False, indent=False):
    if indent:
        _reading_sections.append(INDENT)

    if center:
        _reading_sections.extend([header.center(WIDTH), SECTION_BREAK])
    else:
        _reading_sections.extend([header, SECTION_BREAK])


def _parse_text(text, preserve_line_breaks=False):
    if preserve_line_breaks:
        indented_line_breaks = "".join([LINE_BREAK, INDENT])
        text_lines = text.split(LINE_BREAK)
        _reading_sections.extend([INDENT, indented_line_breaks.join(text_lines),
                                  SECTION_BREAK])
    else:
        wrapped_text = wrap(text, width=WIDTH)
        formatted_text = LINE_BREAK.join(wrapped_text)
        _reading_sections.extend([formatted_text, SECTION_BREAK])
