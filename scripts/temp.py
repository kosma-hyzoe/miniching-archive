import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', "--foobar", action='store_true')
    args = parser.parse_args()

    if args.foobar:
        print("foo")


if __name__ == "__main__":
    main()