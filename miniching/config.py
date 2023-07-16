import os

WIDTH = 80
LINE_BREAK = "\n"
SECTION_BREAK = LINE_BREAK * 2
INDENT = "\t"

default_history_dir: str = os.path.expanduser('$HOME')

HISTORY_PATH: str = r""

TIMESTAMP_FORMAT: str = r"%d-%m-%Y %-H:%M"
HEX_MIRROR: bool = True
