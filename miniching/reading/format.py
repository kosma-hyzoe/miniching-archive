from textwrap import wrap

from miniching.serialization import get_config

try:
    _formats = dict(get_config().items("formats"))
    WIDTH = _formats["width"]
    LINE_BREAK = _formats["line_break"]
    SECTION_BREAK = _formats["section_break"]
    INITIAL_INDENT = _formats["initial_indent"]
    INDENT = _formats["indent"]
except:
    WIDTH = 80
    LINE_BREAK = "\n"
    SECTION_BREAK = LINE_BREAK * 2
    INITIAL_INDENT = ""
    INDENT = 4 * " "


def format_datetime(datetime):
    return datetime.strftime(_formats["timestamp"])
