import os
from textwrap import wrap
from miniching import config as rc

from miniching.reading.helpers import get_result, format_hexagram_title
from miniching.reading.models import Reading, HexagramText, LineText

_DEFAULT_HISTORY_DIR = os.environ["HOME"]
HISTORY_FILENAME = "iching-history.txt"
_reading_sections = []


def write_history(reading: Reading):
    record = []

    record.append(f"{str(reading.timestamp).center(rc.WIDTH)}")

    if len(reading.query) > rc.WIDTH:
        record.append(rc.LINE_BREAK.join(wrap(reading.query.center(
                      rc.WIDTH), rc.WIDTH)))
    else:
        record.append(reading.query.center(rc.WIDTH))

    record.append(get_result(reading.hexagram))

    if not rc.HISTORY_PATH:
        path = os.path.join(_DEFAULT_HISTORY_DIR, HISTORY_FILENAME)
    elif not os.path.isfile(rc.HISTORY_PATH):
        path = os.path.join(rc.HISTORY_PATH, HISTORY_FILENAME)

    else:
        path = rc.HISTORY_PATH

    with open(path, "a+") as f:
        f.write(rc.SECTION_BREAK.join(record))
        f.write(rc.SECTION_BREAK + rc.LINE_BREAK)


def get_printable_reading(reading: Reading) -> str:
    _reading_sections.extend([get_result(reading.hexagram), rc.SECTION_BREAK])

    if reading.trans_text and reading.trans_lines:
        _parse_hexagram(reading.origin_text)
        _reading_sections.append(rc.LINE_BREAK)
        _parse_hexagram(reading.trans_text, reading.lines_to_read)
    elif reading.trans_text:
        _parse_hexagram(reading.origin_text, reading.lines_to_read)
        _reading_sections.append(rc.LINE_BREAK)
        _parse_hexagram(reading.trans_text)
    else:
        _parse_hexagram(reading.origin_text)
    return rc.LINE_BREAK + "".join(_reading_sections)


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
        _reading_sections.append(rc.INDENT)

    if center:
        _reading_sections.extend([header.center(rc.WIDTH), rc.SECTION_BREAK])
    else:
        _reading_sections.extend([header, rc.SECTION_BREAK])


def _parse_text(text, preserve_line_breaks=False):
    if preserve_line_breaks:
        indented_line_breaks = "".join([rc.LINE_BREAK, rc.INDENT])
        text_lines = text.split(rc.LINE_BREAK)
        _reading_sections.extend([rc.INDENT,
                                  indented_line_breaks.join(text_lines),
                                  rc.SECTION_BREAK])
    else:
        wrapped_text = wrap(text, width=rc.WIDTH)
        formatted_text = rc.LINE_BREAK.join(wrapped_text)
        _reading_sections.extend([formatted_text, rc.SECTION_BREAK])
