import argparse
from datetime import datetime

from miniching.modes import get_modes
from miniching.files import write_simple_history, write_map_history
from miniching.excerpts import get_excerpt_with_coin_toss, decode_excerpt, get_reading
from miniching.reading import ReadingParser


def main():
    modes = get_modes()
    now = datetime.now().isoformat(timespec="minutes")

    if modes.quick:
        query = '...'
        timestamp = now
    else:
        timestamp = input("Timestamp:\n\t") if modes.manual_timestamp else now
        query = input("Query:\n\t")
    excerpt = input("Excerpt:\n\t") if modes.evaluate_excerpt else get_excerpt_with_coin_toss()

    decoded_excerpt = decode_excerpt(excerpt)
    reading = get_reading(timestamp, query, decoded_excerpt, modes.classic)

    reading_parser = ReadingParser(reading)
    if not modes.no_print:
        parsed_reading = reading_parser.get_reading_as_printable_output(modes.full_text)
        print(parsed_reading)
    if modes.simple_history:
        parsed_reading = reading_parser.get_reading_as_simple_history_record()
        write_simple_history(parsed_reading)
    if modes.map_history:
        map_record = reading_parser.get_reading_as_map_history_record()
        write_map_history(map_record)


if __name__ == "__main__":
    main()
