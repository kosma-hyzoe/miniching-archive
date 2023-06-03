import argparse
import datetime

from miniching import hexagrams, config
from miniching.reading.compose import compose
from miniching.reading.reading import get_printable_reading, write_history

H_CLASSIC = "use classic evaluation / 'read all changing lines' instead of " \
            "the default modified Zhu Xi method"
H_QUERY = "provide a query instead of using the default input() prompt. " \
          "good for piping but litters the history"
H_EXCERPT = "provide an excerpt using '64' format for pure hexes or '63:1,2' " \
            "with changing lines"
H_TIMESTAMP = "provide a timestamp matching the format specified in config"
H_FULL_READING = "get a full reading"
H_WRITE_HISTORY = "write to iching-history.txt file"
H_SKIP_PRINT = "don't print the reading"


def run():
    pargs = _get_parser_args()

    if pargs.timestamp:
        timestamp = pargs.timestamp
    else:
        timestamp = datetime.datetime.now().strftime(config.TIMESTAMP_FORMAT)

    if pargs.excerpt:
        hexagram = hexagrams.get_from_excerpt(pargs.excerpt, pargs.classic)
    else:
        hexagram = hexagrams.get_with_coin_toss(pargs.classic)

    query = pargs.query if pargs.query else input("Query: ")

    reading = compose(hexagram, timestamp, query)

    if not pargs.skip_print:
        print(get_printable_reading(reading), end="")
    if pargs.write_history:
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
    return parser.parse_args()


if __name__ == "__main__":
    run()
