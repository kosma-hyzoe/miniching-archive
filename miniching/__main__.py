import argparse
from datetime import datetime

from miniching.interface import get_modes, prompt_manual_timestamp
from miniching.files import write_simple_history, write_map_history
from miniching.excerpts import get_excerpt_with_coin_toss, get_decoded_excerpt
from miniching.reading.parse import ReadingParser


def main():
    modes = get_modes()
    now = datetime.now().isoformat(timespec="minutes")

    if modes.quick:
        query = '...'
        timestamp = now
    else:
        # todo validate timestamp
        timestamp = prompt_manual_timestamp() if modes.manual_timestamp else now
        query = input("Query:\n\t")
    excerpt = input("Excerpt:\n\t") if modes.evaluate_excerpt else get_excerpt_with_coin_toss()

    decoded_excerpt = get_decoded_excerpt(excerpt)
    reading_parser = ReadingParser(timestamp, query, decoded_excerpt, modes.classic)

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
