from textwrap import wrap
from miniching.config import WIDTH, LINE_BREAK, SECTION_BREAK, INDENT
from miniching.reading.models import Reading
_parsed_reading = []


def get_history_record(reading: Reading, width):
    record = []

    record.append(f"{str(reading.timestamp).center(WIDTH)}\n")
    if len(reading.query) > WIDTH:
        record.append('\n'.join(wrap(reading.query.center(WIDTH)), width))
    else:
        record.append(reading.query.center(WIDTH))
    


