import argparse
from datetime import datetime

from miniching.divination import get_excerpt_with_coin_toss, get_excerpt_with_yarrow_stalks
from miniching.serialization import write_history, get_config
from miniching.reading.compose import compose_reading
from miniching.reading.format import format_datetime, SECTION_BREAK, INDENT, LINE_BREAK
from miniching.reading.parse import ReadingParser


def main():
    modes = get_modes()
    now = datetime.now()

    if modes.quick:
        query = '...'
        timestamp = format_datetime(now)
    else:
        query = input("Query: ")
        timestamp = prompt_timestamp() if modes.manual_timestamp else format_datetime(now)

    if modes.evaluate_excerpt:
        excerpt = modes.evaluate_excerpt
    elif modes.prompt_excerpt:
        excerpt = input("Excerpt: ")
    elif modes.yarrow_stalks:
        excerpt = get_excerpt_with_yarrow_stalks()
    else:
        excerpt = get_excerpt_with_coin_toss()

    reading = compose_reading(excerpt, timestamp, query, modes.classic)
    reading_parser = ReadingParser(reading)

    if not modes.no_print:
        parsed_reading = reading_parser.get_printable_reading(modes.full_text)
        print(LINE_BREAK + parsed_reading, end="")
    if modes.write_history:
        parsed_reading = reading_parser.get_history_record()
        write_history(parsed_reading)


def prompt_timestamp():
    timestamp = input(f"Timestamp: ")

    try:
        datetime.strptime(timestamp, get_config().get("formats", "timestamp"))
    except ValueError as e:
        print("Error: " + str(e) + " provided in the config file. Please try again.")
        prompt_timestamp()
    else:
        return timestamp


def get_modes():
    parser = argparse.ArgumentParser()

    parser.add_argument('-f', '--full-text', action='store_true', help='get a full reading')
    parser.add_argument('-w', '--write-history', action='store_true', help='write to a history.txt file')
    parser.add_argument('-n', '--no-print', action='store_true', help='skip printing the reading')
    parser.add_argument('-y', '--yarrow-stalks', action='store_true', help='use the yarrow stalks divination method')

    classic_help = "use classic evaluation/'read all changing lines' instead of the default modified Zhu Xi method"
    parser.add_argument('-c', '--classic', action='store_true', help=classic_help)

    quick_help = "get a reading with an empty query and a current timestamp (useful for debugging)"
    parser.add_argument('-q', '--quick', action="store_true", help=quick_help)

    evaluate_help = "provide excerpt using '64' format for pure hexes or '63:1,2' with changing lines"
    parser.add_argument('-e', '--evaluate-excerpt', type=str, default=None, help=evaluate_help)

    parser.add_argument('-p', '--prompt-excerpt', action='store_true', help="prompt for an excerpt")
    parser.add_argument('-t', '--manual-timestamp', action="store_true", help="insert a timestamp with an input prompt")

    return parser.parse_args()


if __name__ == "__main__":
    main()



























