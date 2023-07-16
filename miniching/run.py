import os
import sys
import argparse
import datetime

from miniching import hexagrams, config
from miniching.reading.compose import compose
from miniching.reading.helpers import get_result
from miniching.reading.reading import get_printable_reading, write_history

H_CLASSIC = "use classic evaluation / 'read all changing lines' instead of " \
            "the default modified Zhu Xi method"
H_FULL_READING = "get a full reading instead of just the hexagram transition " \
                  "result"
H_WRITE_HISTORY = "write history to a txt file using the specified "\
                  "path (config.py or command or `-p` argument)."\
                  "will attempt to write in $HOME if no path was specified"
H_SKIP_PRINT = "don't print the reading"
H_QUERY = "provide a query instead of using the default prompt"
H_EXCERPT = "provide an excerpt using '64' /'61:1,2' or the " \
            "3 coin sum notation ('788688' -> 23:3)"
H_TIMESTAMP = "provide a timestamp, any format"
H_HISTORY_PATH = "provide an alternative history path."

E_HISTORY_PATH = "Error: provided path doesn't exist"


def run():
    args = _get_parser_args()

    if args.timestamp:
        timestamp = args.timestamp
    else:
        timestamp = datetime.datetime.now().strftime(config.TIMESTAMP_FORMAT)

    if args.history_path:
        try:
            with open(args.history_path, 'w'):
                pass
        except OSError:
            print(E_HISTORY_PATH, file=sys.stderr)
            sys.exit(1)
        else:
            config.HISTORY_PATH = args.history_path

    if args.excerpt:
        hexagram = hexagrams.get_from_excerpt(args.excerpt, args.classic)
    else:
        hexagram = hexagrams.get_with_coin_toss(args.classic)

    query = args.query if args.query else input("Query: ")

    reading = compose(hexagram, timestamp, query)

    if not args.skip_print:
        if args.full_reading:
            print(get_printable_reading(reading), end="")
        else:
            print(get_result(reading.hexagram, center=False))
    if args.write_history or args.history_path:
        write_history(reading)


def _get_parser_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--classic", action="store_true", help=H_CLASSIC)
    parser.add_argument("-f", "--full-reading", action="store_true",
                        help=H_FULL_READING)
    parser.add_argument("-w", "--write-history", action="store_true",
                        help=H_WRITE_HISTORY)
    parser.add_argument("-s", "--skip-print", action="store_true",
                        help=H_SKIP_PRINT)
    parser.add_argument("-q", "--query", type=str, default=None, help=H_QUERY)
    parser.add_argument("-e", "--excerpt", type=str, default=None,
                        help=H_EXCERPT)
    parser.add_argument("-t", "--timestamp", type=str, default=None,
                        help=H_TIMESTAMP)
    parser.add_argument("-p", "--history-path", type=str, default=None,
                        help=H_HISTORY_PATH)
    return parser.parse_args()

