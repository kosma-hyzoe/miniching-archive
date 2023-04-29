import os
from textwrap import wrap
from miniching.config import WIDTH, LINE_BREAK, SECTION_BREAK, INDENT
from miniching.config import HISTORY_PATH 

from miniching.reading.format import get_result
from miniching.reading.models import Reading


_DEFAULT_HISTORY_DIR = os.environ["HOME"]
_parsed_reading = []


def write_history(reading, width):
    record = []

    record.append(f"{str(reading.timestamp).center(WIDTH)}\n")
    
    if len(reading.query) > WIDTH:
        record.append("\n".join(wrap(reading.query.center(WIDTH), width)))
    else:
        record.append(reading.query.center(WIDTH))

    record.append(get_result(reading.hexagram).center(WIDTH))

    if not HISTORY_PATH:
        path = os.path.join(_DEFAULT_HISTORY_DIR, "iching-history.txt")
    elif not os.path.isfile(HISTORY_PATH):
        path = os.path.join(HISTORY_PATH, "iching-history.txt")

    with open(HISTORY_PATH, "a+") as f:
        f.write("\n".join(record) + "\n")
