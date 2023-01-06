import argparse
from datetime import datetime

from miniching.iching import get_excerpt_with_coin_toss, decode_excerpt, get_reading
from miniching.files import write_simple_history, write_map_history
from miniching.reading_parser import ReadingParser


def main():
    modes = get_parser_args()
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


def get_parser_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('-f', '--full-text', action='store_true', help='get a full reading')
    parser.add_argument('-s', '--simple-history', action='store_true', help='write to a simple history file')
    parser.add_argument('-m', '--map-history', action='store_true', help='write to a map history file')
    parser.add_argument('-n', '--no-print', action='store_true', help='skip printing the reading')

    classic_help = "use classic evaluation/'read all changing lines' instead of the default modified Zhu Xi method"
    parser.add_argument('-c', '--classic', action='store_true', help=classic_help)
    quick_help = "get a reading with an empty query and a current timestamp (useful for debugging)"
    parser.add_argument('-q', '--quick', action="store_true", help=quick_help)
    evaluate_help = "get reading with prompted excerpt using '64' format for pure hexes or '63:1,2' with changing lines"
    parser.add_argument('-e', '--evaluate-excerpt', action='store_true', help=evaluate_help)

    parser.add_argument('-t', '--manual-timestamp', action="store_true", help="insert a timestamp with an input prompt")

    return parser.parse_args()


if __name__ == "__main__":
    main()
