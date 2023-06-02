import argparse
import sys
from datetime import datetime

from miniching import hexagrams, config
from miniching.reading.compose import compose
from miniching.reading.helpers import format_timestamp
from miniching.reading.parse_old import ReadingParser, LINE_BREAK


def run():
    pargs = _get_parser_args()
    now = format_timestamp(datetime.now())

    timestamp = format_timestamp(pargs.timestamp) if pargs.timestamp else now
    query = pargs.query if pargs.query else input("Query")

    if pargs.excerpt:
        hexagram = hexagrams.get_from_excerpt(pargs.excerpt, pargs.classic)
    else:
        hexagram = hexagrams.get_with_coin_toss(pargs.classic)

    reading = compose(hexagram, timestamp, query)
    reading_parser = ReadingParser(reading)

    if not pargs.skip_print:
        parsed_reading = reading_parser.get_printable_reading(
            pargs.full_reading)
        print(LINE_BREAK + parsed_reading, end="")
    if pargs.write_history:
        parsed_reading = reading_parser.get_history_record()
        # TODO
        # write_history(parsed_reading)


def _get_parser_args():
    parser = argparse.ArgumentParser()
    help = "use classic evaluation / 'read all changing lines' instead of the default modified Zhu Xi method"
    parser.add_argument("-c", "--classic", action="store_true", help=help)
    parser.add_argument(
        "-f", "--full-reading", action="store_true", help="get a full reading"
    )
    parser.add_argument(
        "-w", "--write-history", action="store_true", help="write to a history.txt file"
    )
    parser.add_argument(
        "-s", "--skip-print", action="store_true", help="don't print the reading"
    )

    help = "provide a query instead of using the default input() prompt. good for piping but litters the history"
    parser.add_argument("-q", "--query", type=str, default=None, help=help)
    help = "provide an excerpt using '64' format for pure hexes or '63:1,2' with changing lines"
    parser.add_argument("-e", "--excerpt", type=str, default=None, help=help)
    help = "provide a timestamp matching the format specified in config"
    parser.add_argument("-t", "--timestamp", type=str, default=None, help=help)

    return parser.parse_args()


if __name__ == "__main__":
    run()
