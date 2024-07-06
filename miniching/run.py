import os
import sys
import argparse
import datetime

from miniching import hexagrams
from miniching.reading.compose import compose
from miniching.reading.helpers import get_result
from miniching.reading.reading import get_printable_reading, print_last

TIMESTAMP_FORMAT = r"%d-%m-%Y %-H:%M"
HISTORY_FILENAME = "iching-history.txt"
DEFAULT_HISTORY_DIR = os.environ["HOME"]
WIDTH = 80

H_CLASSIC = "use classic evaluation / 'read all changing lines' instead of " \
    "the default modified Zhu Xi method"
H_FULL_READING = "get full reading instead of just the hexagram transition " \
    "result"
H_SKIP_WRITE = "don't write to history path, even if -w or -p flags were" \
    "provided"
H_QUERY = "provide a query instead of using the default prompt or posix" \
    "redirection"
H_EXCERPT = "provide an excerpt using '64' /'61:1,2' or the " \
            "3 coin sum notation ('788688' -> 23:3)"
H_TIMESTAMP = "provide a timestamp, any format"
H_OUTPUT = "Provide an alternative history path, file or dir"
H_ASCII_HEX = "Use hexadecimal ascii characters next to the hexagram numbers"
H_PRINT_LAST = "Use hexadecimal ascii characters next to the hexagram numbers"


def run():
    args = _get_parser_args()

    if args.print_last:
        reading

    if args.timestamp:
        timestamp = args.timestamp
    else:
        timestamp = datetime.datetime.now().strftime(TIMESTAMP_FORMAT)

    if args.output:
        try:
            with open(args.output, 'w'):
                pass
        except OSError:
            if os.path.isdir(args.output) and os.path.exists(args.output):
                output = open(os.path.join(args.output, HISTORY_FILENAME), 'w')
            else:
                print("Error: provided path is invalid", file=sys.stderr)
                sys.exit(1)
        else:
            output = args.history_path

    if args.excerpt:
        hexagram = hexagrams.get_from_excerpt(args.excerpt, args.classic)
    else:
        hexagram = hexagrams.get_with_coin_toss(args.classic)

    query = args.query if args.query else input("Query: ")

    reading = compose(hexagram, timestamp, query)

    if args.full_reading:
        print(get_printable_reading(reading), end="", file=output)
    else:
        print(get_result(reading.hexagram, center=False), file=output)


def _get_parser_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--classic", action="store_true", help=H_CLASSIC)
    parser.add_argument("-f", "--full-reading", action="store_true",
                        help=H_FULL_READING)
    parser.add_argument("-s", "--skip-write", action="store_true",
                        help=H_SKIP_WRITE)
    parser.add_argument("-q", "--query", type=str, default=None, help=H_QUERY)
    parser.add_argument("-e", "--excerpt", type=str, default=None,
                        help=H_EXCERPT)
    parser.add_argument("-t", "--timestamp", type=str, default=None,
                        help=H_TIMESTAMP)
    parser.add_argument("-o", "--output", type=str, default=None,
                        help=H_OUTPUT)
    parser.add_argument("-a", "--asci-hex", action="store_true",
                        help=H_ASCII_HEX)
    parser.add_argument("-l" "--print-last", action="store_true",
                        help=H_PRINT_LAST)
    return parser.parse_args()
