import argparse
from datetime import datetime

from miniching import interface
from miniching.files import write_simple_history, write_map_history
from miniching.divination import get_excerpt_with_coin_toss
from miniching.reading.compose import compose_reading
from miniching.reading.format import format_datetime
from miniching.reading.parse import ReadingParser


def main():
    modes = interface.get_modes()
    now = datetime.now()

    if modes.quick:
        query = '...'
        timestamp = format_datetime(now)
    else:
        # todo validate timestamp
        timestamp = interface.prompt_manual_timestamp() if modes.manual_timestamp else format_datetime(now)
        query = input("Query:\n\t")

    excerpt = input("Excerpt:\n\t") if modes.evaluate_excerpt else get_excerpt_with_coin_toss()

    reading = compose_reading(excerpt, timestamp, query, modes.classic)
    reading_parser = ReadingParser(reading)

    if not modes.no_print:
        parsed_reading = reading_parser.get_printable_reading(modes.full_text)
        print(parsed_reading)
    if modes.simple_history:
        parsed_reading = reading_parser.get_reading_as_simple_history_record()
        write_simple_history(parsed_reading)
    if modes.map_history:
        map_record = reading_parser.get_reading_as_map_history_record()
        write_map_history(map_record)


if __name__ == "__main__":
    main()
