from miniching.run import run

if __name__ == "__main__":
    try:
        run()
    except EOFError:
        exit(0)