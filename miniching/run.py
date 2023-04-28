import argparse
import sys
from datetime import datetime

from miniching import hexagrams, config
from miniching.serialization import write_history
from miniching.reading.compose import compose
from miniching.reading.format import format_datetime
from miniching.reading.parse_old import ReadingParser, LINE_BREAK


def run():
    parser_args = _get_parser_args()
    now = format_datetime(datetime.now())

    if parser_args.timestamp:
        timestamp = parser_args.timestamp
    else:
        timestamp = now

    if parser_args.query:
        query = parser_args.query
    else:
        query = input("Query: ")

    if parser_args.excerpt:
        hexagram = hexagrams.get_from_excerpt(parser_args.excerpt)
    else:
        hexagram = hexagrams.get_with_coin_toss()

    reading = compose(hexagram, timestamp, query, parser_args.classic)
    reading_parser = ReadingParser(reading)

    if not parser_args.skip_print:
        parsed_reading = reading_parser.get_printable_reading(parser_args.full_reading)
        print(LINE_BREAK + parsed_reading, end="")
    if parser_args.write_history:
        parsed_reading = reading_parser.get_history_record()
        write_history(parsed_reading)


def _get_parser_args():
    parser = argparse.ArgumentParser()

    classic_help = "use classic evaluation / 'read all changing lines' instead of the default modified Zhu Xi method"
    parser.add_argument("-c", "--classic", action="store_true", help=classic_help)

    parser.add_argument(
        "-f", "--full-reading", action="store_true", help="get a full reading"
    )
    parser.add_argument(
        "-w", "--write-history", action="store_true", help="write to a history.txt file"
    )
    parser.add_argument(
        "-s", "--skip-print", action="store_true", help="don't print the reading"
    )

    query_help = "provide a query instead of using the default input() prompt. good for piping but litters the history"
    parser.add_argument("-q", "--query", type=str, default=None, help=query_help)
    excerpt_help = "provide an excerpt using '64' format for pure hexes or '63:1,2' with changing lines"
    parser.add_argument("-e", "--excerpt", type=str, default=None, help=excerpt_help)
    timestamp_help = (
        "provide a timestamp matching the provided format (by default it's %%d-%%m-%%Y)"
    )
    parser.add_argument(
        "-t", "--timestamp", type=str, default=None, help=timestamp_help
    )

    return parser.parse_args()


if __name__ == "__main__":
    run()
