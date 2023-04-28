import os
from textwrap import wrap
from miniching import config
from miniching.config import WIDTH, LINE_BREAK, SECTION_BREAK, INDENT
from miniching.reading.models import Reading


_DEFAULT_HISTORY_DIR = os.environ['HOME']
_parsed_reading = []
    

def write_history(reading: Reading, width, path=config.HISTORY_PATH):
    record = []

    record.append(f"{str(reading.timestamp).center(WIDTH)}\n")
    if len(reading.query) > WIDTH:
        record.append('\n'.join(wrap(reading.query.center(WIDTH)), width))
    else:
        record.append(reading.query.center(WIDTH))
    
    if not path or path == 'default': 
        path = os.path.join(_DEFAULT_HISTORY_DIR, "iching-history.txt")
    elif not os.path.isfile(path):
        path = os.path.join(path, "iching-history.txt")

    with open(path, "a+") as f:
        f.write(record)


