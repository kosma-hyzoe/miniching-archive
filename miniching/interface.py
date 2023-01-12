import argparse

from miniching.reading.parse import ReadingParser


def prompt_query():
    query = input("Query:\n\t")
    print(ReadingParser.section_break)
    return query


def prompt_manual_timestamp():
    pass


def get_modes():
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