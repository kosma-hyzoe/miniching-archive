import os

WIDTH = 80
LINE_BREAK = "\n"
SECTION_BREAK = LINE_BREAK * 2
INDENT = 2 * " "

default_history_dir = os.path.expanduser('~')

HISTORY_DIR: str = r""

TIMESTAMP_FORMAT = r"%d-%m-%Y"
UNICODE_HEXAGRAM_MIRROR: bool = True
