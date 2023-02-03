# miniching
#### [Click here for a video demo](https://www.youtube.com/watch?v=K6esbD3UZlk)

## IMPORTANT DISCLAIMER
This version was created as a final project for Harvard's
[CS50x](https://www.edx.org/course/introduction-computer-science-harvardx-cs50x) course.
It works, but it's quite clunky - consider it pre-alpha.
I decided to leave it here for a while for reference, but I DO NOT recommend using it.
Check out the `main` branch instead.

---
## What is miniching?
A console-friendly, minimalist I Ching package written in Python 3. It's most notable, unique feature is the map history
which groups the user's history entries by the hexagrams instead of simply sorting them by ascending date. 

### How to run minichig?
__To run the package__:
1. Make sure Python 3 is installed. The project was developed on Python 3.10.6.
Older and newer versions should also work, but were not tested.
2. Install the requirements from `requirements.txt` (currently it only contains `pyyaml==6.0`)
3. Navigate to where the `miniching` package is located (a `pip`-installable package coming soon)
4. Modify the `config.ini` file if needed (for now it only has the `SIMPLE_HISTORY_DIR` and `MAP_HISTORY_DIR` variables)
5. Run `$ python3 -m miniching` in console with chosen flags/arguments.
The arguments specify "modes" that modify evaluation process, the result received and writing to external history files.
All arguments store true/false values only, some run additional `input()` prompts. 
The arguments are parsed via the built-in Python `argparse` module, so there's a proper `-h/--help`:
```
usage: __main__.py [-h] [-f] [-s] [-m] [-n] [-c] [-q] [-e] [-t]

options:
  -h, --help            show this help message and exit
  -f, --full-text       get a full reading
  -s, --simple-history  write to a simple history file
  -m, --map-history     write to a map history file
  -n, --no-print        skip printing the reading
  -c, --classic         use classic evaluation/'read all changing lines' instead of the default modified Zhu Xi method
  -q, --quick           get a reading with an empty query and a current timestamp (useful for debugging)
  -e, --evaluate-excerpt
                        get reading with prompted excerpt using '64' format for pure hexes or '63:1,2' with changing lines
  -t, --manual-timestamp
                        insert a timestamp with an input prompt
```

### How does miniching work?
There's a `__main__.py` file that parses the arguments and runs the three main files based on them:
* `iching.py` - contains methods responsible for generating a hexagram excerpt via emulating the coin toss, decoding the
excerpt and getting a `reading` dictionary containing the relevant text. 
* `reading_parser.py` - contains a `ReadingParser` class responsible for parsing the reading to a printable string or
a history file.
* `files.py` - contains methods for reading configuration and I Ching resources and writing the history. it stores the
resource files' values (dictionaries) as runtime constants, i.e.  `REFERENCE = read_serialization_data(RESOURCES_DIR + "reference.yaml")`

---
## What is I Ching?
An ancient divination and wisdom book, probably the most influential text of chinese history.
Think jungian dream generator and Bible studies for the cool kids or a less woo-woo Tarot.

### Isn't it still a bit esoteric and weird?
__It probably is.__ I hope that mentioning Jung makes it digestible enough for an average western intellectual. Here's his
I Ching foreword at [carljungdepthpsychologysite.blog](https://carljungdepthpsychologysite.blog/2020/02/03/foreword-to-the-i-ching-by-carl-gustav-jung/)


### How does I Ching divination work?
The user writes down a query (usually a question) and gets a result with one of the divination methods -
usually tossing coins or arranging yarrow stalks.

The main part of the text consists of 64 hexagrams.
Their signs consist of six lines - yin ("unbroken") and yang ("broken") ones.

When tossing coins, each coin is assigned a value of 3 (usually "heads") or 2 (usually "tails").
A 7 or 8 gets you "old" yin and yang, a 9 or 6 gets you a "new" yin and yang and produce changing lines.

The result to a query can either pe a "pure" hexagram, (i.e. 3 : ䷂) or a hexagram transition if one or more changing
lines apply (i.e. 3 -> 27 : ䷂ -> ䷚, where changing lines are 5th and 6th).  The user should now read all of related text using preferred evaluation method. 

_This is of course nothing but a major simplification_

---
### Credits and references:
* The modified Zu Xhi evaluation method that miniching uses by default is from [biroco.com](https://www.biroco.com/yijing/basics.htm)
* The default `iching_reference.yaml` file (more translations coming soon)
is the classic Richard Wilhelm's and Cary F. Baynes' translation. I found it as a JSON file in a public
[GitHub repo of a user called `dkloke`](https://github.com/dkloke/I-Ching-ref/blob/master/iChing.json), converted it to YAML and edited for my needs.

### Recommended sources for an in-depth reference:
* [Wikipedia](https://en.wikipedia.org/wiki/I_Ching)
* [Biroco](https://www.biroco.com/yijing/index.htm)
* [The Gnostic Book Of Changes](https://www.jamesdekorne.com/GBCh/GBCh.htm)
* [Carl Jung and the I Ching](https://carl-jung.net/iching.html)
